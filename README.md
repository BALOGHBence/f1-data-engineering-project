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

Historical data about F1 races is available at https://ergast.com/mrd/. To get the data, you can use the API or download the files manually as a compressed folder alongside a user manual and the entity relationship diagram. All of this can be found in the `data` folder of this repository. Before using this data, you should read the 'terms ans conditions' section of the Ergast API.

### Project requirements

### Solution architecture