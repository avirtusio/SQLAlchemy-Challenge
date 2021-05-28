import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from datetime import timedelta


engine = create_engine("sqlite://Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflec = True)
Measurement = Base.classes.measurement 
Station = Base.classes.station
session = Session(engine)




app = Flask(_name_)

@app.route("/")
def Home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipation")
def percipitation():
    session = Session(engine)
    date_last = session.query(Measurement.date).order_by(Measurement.date.desc()).first.date
    date_last = dt.datetime.strptime(date_last, "%Y-%m-%d")
    date_first = date_last - timedelta(days = 365)
    percipitation_results = (session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_first).order_by(Measurement.date).all())
    return jsonify(percipitation_results)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_results = session.query(Station.station, Station.name).all()
    return jsonify(stations_results)

@app.route("/api//v1.0/tobs")
def tobs():
    session = Session(engine)
    date_last = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    date_last = dt.datetime.strptime(date_last, "%Y-%m-%d")
    date_first = date_last - timedelta(days = 365)
    station_counts = (session.query(Measurement.station, func.count).filter(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    top_station = (station_counts[0])
    top_station = (top_station[0])
    session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station == top_station).all()
        top_station_year_obs = sessions.query(Measurement.tobs).\
        filter(Measurement.station == top_station).filter(Measurement.date >= date_first).all()
        return jsonify(top_station_year_obs)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def start(start = none, end = none):
    session = Session(engine)


if _name_ == '_main_':
    app.run()


