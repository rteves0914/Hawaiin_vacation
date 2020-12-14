# Import all dependencies and packages
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates and precipitation values based on dates
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Convert dates and precipitation into a dictionary
    date_precip = []
    for date, precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = precipitation
        date_precip.append(precipitation_dict)

    return jsonify(date_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all the station names
    station_results = session.query(Station.station).all()
    session.close()

    # Create a list of all station names and return as JSON
    all_stations = []
    for station in station_results:
        all_stations.append(station)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates and temperature observation values for the past year at 'USC00519281'
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= one_year).\
    filter(Measurement.station == 'USC00519281').all()
    session.close()

    # Create a list of all tobs for previous year and return as JSON
    all_temp = []
    for temperature in temp_results:
        all_temp.append(temperature)

    return jsonify(all_temp)



if __name__ == '__main__':
    app.run(debug=True)
