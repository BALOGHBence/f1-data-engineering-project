import os
import pandas as pd
import flask, dash
from dash import dcc, html, Input, Output, callback, dash_table, ctx, no_update
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from databricks.sdk.core import Config
from databricks import sql

from dotenv import load_dotenv

load_dotenv()

print()

# Ensure environment variable is set correctly
assert os.getenv('DATABRICKS_WAREHOUSE_ID'), "DATABRICKS_WAREHOUSE_ID must be set in app.yaml."
#assert os.getenv('ENV'), "ENV must be set in app.yaml."

ENV = "dev" #os.getenv("ENV")

catalog="bence-balogh-catalog"
schema = f"f1-{ENV}" if ENV else "f1"

# Databricks config
cfg = Config()


# Query the SQL warehouse with Service Principal credentials
def sql_query_with_service_principal(query: str) -> pd.DataFrame:
    """Execute a SQL query and return the result as a pandas DataFrame."""
    with sql.connect(
        server_hostname=cfg.host,
        http_path=f"/sql/1.0/warehouses/{cfg.warehouse_id}",
        credentials_provider=lambda: cfg.authenticate  # Uses SP credentials from the environment variables
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall_arrow().to_pandas()


# Query the SQL warehouse with the user credentials
def sql_query_with_user_token(query: str, user_token: str) -> pd.DataFrame:
    """Execute a SQL query and return the result as a pandas DataFrame."""
    with sql.connect(
        server_hostname=cfg.host,
        http_path=f"/sql/1.0/warehouses/{cfg.warehouse_id}",
        access_token=user_token  # Pass the user token into the SQL connect to query on behalf of user
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall_arrow().to_pandas()


def load_data_with_user_token(query:str) -> pd.DataFrame:
    try:
        # Extract user access token from the request headers
        user_token = flask.request.headers.get('X-Forwarded-Access-Token')
        if not user_token:
            raise Exception("Missing access token in headers.")
        return sql_query_with_user_token(query, user_token=user_token)
    except Exception as e:
        print(f"Data load failed: {str(e)}")
        return pd.DataFrame()
    
    
def load_data_with_service_principal(query:str) -> pd.DataFrame:
    try:
        return sql_query_with_service_principal(query)
    except Exception as e:
        print(f"Data load failed: {str(e)}")
        return pd.DataFrame()
    

def get_driver_standings(year:str) -> pd.DataFrame:
    """Fetch driver standings data from the SQL warehouse."""
    query = f"""
    SELECT 
        driver,
        points
    FROM `{catalog}`.`{schema}`.gold_tbl_driver_standings 
    WHERE year = '{year}'"""
    return load_data_with_service_principal(query)


def get_constructor_standings(year:str) -> pd.DataFrame:
    """Fetch driver standings data from the SQL warehouse."""
    query = f"""
    SELECT 
        constructor,
        points
    FROM `{catalog}`.`{schema}`.gold_tbl_constructor_standings 
    WHERE year = '{year}'"""
    return load_data_with_service_principal(query)
    

query = "SELECT * FROM `bence-balogh-catalog`.`f1-dev`.gold_tbl_driver_standings"
df_driver_standings: pd.DataFrame = load_data_with_service_principal(query)
df_years = df_driver_standings[["year"]].drop_duplicates().sort_values(by="year", ascending=False)
years = df_years["year"].to_list()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dcc.Store(id='page-load-trigger', data=0),
    dbc.Row([
        dbc.Col([
            html.A("Open Documentation", href="static/docs/index.html", target="_blank"),
            dcc.Dropdown(years, years[0], id='dropdown-years'),
            dcc.Tabs(
                id="tabs-standings", value='tab-drivers-standings', 
                children=[
                    dcc.Tab(label='Drivers', value='tab-drivers-standings'),
                    dcc.Tab(label='Standings', value='tab-constructors-standings'),
                ]
            ),
            html.Div(id='tabs-standings-content')
        ], width=12)
    ])
], fluid=True)


@callback(
    Output('tabs-standings-content', 'children'),
    Input('tabs-standings', 'value'),
    Input('dropdown-years', 'value'),
)
def render_content(tab_value:str, year:str) -> dash_table.DataTable:
    if not ctx.triggered_id:
        return no_update
    
    if tab_value == 'tab-drivers-standings':
        df: pd.DataFrame = get_driver_standings(year)
        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    elif tab_value == 'tab-constructors-standings':
        df: pd.DataFrame = get_constructor_standings(year)
        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])


if __name__ == "__main__":
    app.run(debug=True, port=8051)