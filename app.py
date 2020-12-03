# ---------------------------------
# Import Dependancies
# ---------------------------------
# General Dependancies
import datetime as dt
import numpy as np
import pandas as pd

# SQLAlchemy Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask Dependency
from flask import Flask, jsonify



# ---------------------------------
# 9.5.1 Set Up Flask
# ---------------------------------
# SQLAlchemy Create Engine - provides ability to querry hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into the new model
# relfect = transfer the contents of the database into a different structure of data
Base = automap_base()


# reflect the tables
# (reflects the schema from the tables to the code)
Base.prepare(engine, reflect=True)


# Save references to each table
# to reference the station class, use Base.classes.station
# Since it can be rather cumbersome to type Base.classes every time 
# we want to reference the measurement or station classes, 
# we can give the classes new variable names, Measurement and Station. 
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create session (link) from Python to the DB
# This session allows to query for data.  
session = Session(engine)


# Set up Flask - Create a New Flask App Instance called app (_Magic Method_)
app = Flask(__name__)


# ---------------------------------
# 9.5.2 Create Flask Welcome Route
# ---------------------------------
# Create route:
@app.route("/")


# Add function 
# which provides the routing information for other routes. 
# Return statement has f-strings as reference to other routes. 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end
    ''')


# ---------------------------------
# 9.5.3 Create Precipitaton Route
# ---------------------------------
# Create route:
@app.route("/api/v1.0/precipitation")

# Add function:
def precipitation():
     # Calculate the date one year from W. Avy's fav date.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)   
    # Query to retrieve date and precipitation data
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()                 
    # Use jsonify() to format the function/dictionary results into a JSON file. 
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


# ---------------------------------
# 9.5.4 Create Stations Route
# ---------------------------------
# Create route:
@app.route("/api/v1.0/stations")

# Add function:
def stations():
    # Stations available in the dataset
    results = session.query(Station.station).all()
    # Unravel results into 1-dimensional array using np.ravel() funciton with results as paramater. 
    # Convert results to a list, use list() function.  
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


# ---------------------------------
# 9.5.5 Monthly Temperature Route
# ---------------------------------
# Create route:
@app.route("/api/v1.0/tobs")

# Add function:
def temp_monthly():
    # Calculate the date one year from W. Avy's fav date.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)  
    # From station with highest # observations (USC...281), querry temps from prev_year time frame. 
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # Unravel results into 1-dimensional array using np.ravel() funciton with results as paramater. 
    # Convert results to a list, use list() function.  
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


# ---------------------------------
# 9.5.6 Create Statistics Route
# ---------------------------------
# Create route:
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Add function:
def stats(start=None, end=None):
    #     Create querry form temp min, max and avg.  Create list sel
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # to determine the starting and ending date, add an if-not statement
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
    # * above indicates multiple results for the querry: min, avg and max temperatures. 




# ============================
# # In Anaconda Powershell

# # set FLASK_APP=app.py
# # flask run
# ============================
