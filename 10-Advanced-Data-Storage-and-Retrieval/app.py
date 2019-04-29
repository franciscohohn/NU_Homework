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
           f"/api/v1.0/(Start(yyyy-mm-dd))<br/>"
           f"/api/v1.0/(Start(yyyy-mm-dd))/(End(yyyy-mm-dd))<br/>"
           )

@app.route("/api/v1.0/precipitation")
def calc_temps():
    prcp_query=session.query(Measurement.date, Measurement.prcp, Measurement.station).filter(Measurement.date.between("2016-08-23", "2017-08-23")).all()
    pcrp_list=[]
    for row in range(len(prcp_query)):
        prcp_dict = {}
        prcp_dict["date"] = prcp_query[row][0]
        prcp_dict["prcp"] = prcp_query[row][1]
        prcp_dict["station"] = prcp_query[row][2]
        pcrp_list.append(prcp_dict)
    return jsonify(pcrp_list)

@app.route("/api/v1.0/stations")
def stations():
    
    print("Server received for 'stations' page...")
    return jsonify(session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all())

@app.route("/api/v1.0/tobs")
def tobs():
    
    print("Server received for 'tobs' page...")

    return jsonify(session.query(Measurement.date, Measurement.tobs).filter(Measurement.date== '2017-08-23').all())

@app.route("/api/v1.0/<start_date>/")
def temp_start(start_date):
    
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).first()
    
    temps_dict1 = {"TMIN": temps[0], "TMAX": temps[1], "TAVG": round(temps[2],2)}
    return jsonify(temps_dict1)

@app.route("/api/v1.0/<start_date>/<end_date>/")
def temp_range(start_date, end_date):
    
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date)).first()
    
    temps_dict2 = {"TMIN": temps[0], "TMAX": temps[1], "TAVG": round(temps[2],2)}
    return jsonify(temps_dict2)

if __name__ == '__main__':
    app.run(debug=True)

    