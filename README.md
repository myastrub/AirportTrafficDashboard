# Airport Traffic Dashboard

## Introduction
This is a small pet project aiming at exploring Python and its frameworks (mainly Dash and Pandas) to create dashboards. 
My goal is just to create a small dashboard to present information about airport traffic in Europe in a nice and interactive way.
The information comes from Aviation Intelligence Portal provided by EUROCONTROL:
https://ansperformance.eu/data/

## Technologies used
The app is built using:
* Pandas and NumPy to load and process data
* Dash to visualise the data
* Dash bootstrap components to make sure that the dashboard has a responsive layout
* SciPy to smooth the data on the graphs
All needed packaged and dependencies are listed in the 'requirements.txt' file.

## Deployment
The dashboard is deployed on Heroku:
https://airport-traffic-dashboard.herokuapp.com/

The 'Procfile' and 'runtime.txt' files are needed for Heroku deployment.

## Future developments
A few things can be improved on the dashboard:
* Daily average per state can be enhanced to include not only information from one day but from a period
* Seasonal availability chart can be squeezed to add another chart into the dashboard
* Style of the tables can be improved