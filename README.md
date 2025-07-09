# Data Engineering Capstone Project using F1 Data

## Project overview

## Key concepts of F1

- There is a F1 season once every year.
- Every season consists of a couple of races.
- Every race happens over a weekend (from friday to sunday), called a race weekend. During the weekend, there are practice sessions, qualifiers (to decide the grid positions of the drivers for the race on sunday) and the race. Points are only given for the results of the race, other events are not scored by points.
- A race consists of laps and pit stops. A pit stop is when a driver goes out to the pit to change tires or to repair a damaged part, etc. Different circuits have a different number of laps to be completed.
- Every race weekend belongs to a certain race circuit.
- Normally there is one F1 race at a race circuit, but in extreme cases there can me more than one (for instance, at the time of the COVID outbreak in 2020, some circuits were nogo, so other circuits had to take more more than one).
- There are teams like Ferrari or Mercedes and every team has two drivers. Every driver has a number assigned to him.
- The drivers are racing for the Drivers championship title, and the teams are contesting for the Constructors title.
- At every race weekend, drivers are ranked based on their position at the end of the race. Obviously, the winner gets the most points. The points of the drivers are added to their individual cumulative scores and to their respective teams cumulative scores as well. These tables are called `Friver Standings` and `Constructor Standings`
- At the end of the season, whichever driver has the most points, wins the driver's championship title, and the team with the most points wins the constructor's championship title.

### Source data

Historical data about F1 races is available at <https://ergast.com/mrd/>. To get the data, you can use the API or download the files manually as a compressed folder alongside a user manual and the entity relationship diagram. All of this can be found in the `data` folder of this repository. Before using this data, you should read the 'terms ans conditions' section of the Ergast API.

## Installation

```shell
poetry lock
poetry install [--with docs]
```

On MacOS:

```shell
cd app
python3 -m venv .venv
source .venv/bin/activate
deactivate
```

On Windows

```shell
cd app
python -m venv .venv
.venv/scripts/activate
deactivate
```

### Solution architecture

## Deployment Workflow

1. Install the Databricks CLI from <https://docs.databricks.com/dev-tools/cli/databricks-cli.html>

2. Authenticate to your Databricks workspace, if you have not done so already:

    ``` shell
    databricks configure
    ```

3. To deploy a development copy of this project, type:

    ``` shell
    databricks bundle deploy --target dev
    ```

    (Note that "dev" is the default target, so the `--target` parameter
    is optional here.)

    This deploys everything that's defined for this project.
    For example, the default template would deploy a job called
    `[dev yourname] my_project_job` to your workspace.
    You can find that job by opening your workpace and clicking on **Workflows**.

4. Similarly, to deploy a production copy, type:

   ``` shell
   databricks bundle deploy --target prod
   ```

   Note that the default job from the template has a schedule that runs every day
   (defined in resources/my_project.job.yml). The schedule
   is paused when deploying in development mode (see
   <https://docs.databricks.com/dev-tools/bundles/deployment-modes.html>).

5. To run a job or pipeline, use the "run" command:

   ``` shell
   databricks bundle run
   ```

6. Optionally, install developer tools such as the Databricks extension for Visual Studio Code from
   <https://docs.databricks.com/dev-tools/vscode-ext.html>.

7. For documentation on the Databricks asset bundles format used
   for this project, and for CI/CD configuration, see
   <https://docs.databricks.com/dev-tools/bundles/index.html>.
