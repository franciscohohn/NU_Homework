# %matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

# import Flask
from flask import Flask, jsonify
import numpy as np
import pandas as pd

# import datetime as dt
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# create an app
app = Flask(__name__)

# start_date = input(str("Start date (yyyy-mm-dd): "))
# end_date = input(str("End date (yyyy-mm-dd): "))

# define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received for 'Home' page...")
    return ("Welcome to my 'Home' page!<br/>"
           f"Available Routes:<br/>"
           f"/api/v1.0/precipitation<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/<start><br/>"
           f"/api/v1.0/<start>/<end><br/>"
           )


@app.route("/api/v1.0/precipitation")
def calc_temps():
# def calc_temps(start_date, end_date):
    
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    print("Server received for 'precipitation' page...")
    
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).all())\
#         filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
# print(calc_temps(start_date, end_date))

@app.route("/api/v1.0/stations")
def stations():
    
    print("Server received for 'stations' page...")
    return jsonify(session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all())

@app.route("/api/v1.0/tobs")
def tobs():
    
    print("Server received for 'tobs' page...")

    return jsonify(session.query(Measurement.date, Measurement.tobs).filter(Measurement.date== '2017-08-23').all())

@app.route("/api/v1.0/<start>")
def start_only():
    
    print("Server received for 'start_only' page...")

    return("Works")

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    
    print("Server received for 'start_end' page...")

    return("Works")


if __name__ == '__main__':
    app.run(debug=True)

    
# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.


# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)


# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation

