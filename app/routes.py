from app import app, async_session
from app.utils import flatten_data, calc_averages
from app.models import Measurement, Forecast, Station, Sensor
from flask import jsonify, request
from sqlalchemy.sql import select, update, delete
from sqlalchemy.exc import IntegrityError
from datetime import date
from markupsafe import escape
from sqlalchemy.orm import aliased, Session
from sqlalchemy import and_, cast, Date

@app.route('/')
@app.route('/health')
def index():
    return "up", 200

@app.route('/measurements')
async def get_data():
    async with async_session() as session:
        stmt = select(Measurement).order_by(Measurement.date)
        result = await session.execute(stmt)
        data = result.fetchall()
        return jsonify([tuple(row) for row in data])


@app.route('/ingest', methods=['POST'])
async def ingest_data():
    try:
        content = request.json
        flattened = flatten_data(content)
        M = Measurement(**flattened)
        async with async_session() as session:
            async with session.begin():
                session.add(M)
                return jsonify(M), 201
    except TypeError as e:
        return {"error": f"Malformed data: {e}"},  400
    except IntegrityError as e:
        return {"error": f"Integrity Error: {e}"},  400


@app.route('/forecast', methods=['POST'])
async def add_forecast():
    try:
        F = Forecast(**request.json)
        async with async_session() as session:
            async with session.begin():
                session.add(F)
                return jsonify(F), 201
    except TypeError as e:
        return {"error": f"Malformed data: {e}"},  400
    except IntegrityError as e:
        return {"error": f"Integrity Error: {e}"},  400


@app.route('/forecast/<city>/<usrdate>', methods=['GET'])
async def get_forecast(city, usrdate):
    try:
        target_date = date.fromisoformat(escape(usrdate))
        async with async_session() as session:
            async with session.begin():
                # get forecast data
                stmt = select(Forecast).where(Forecast.forecast_date == target_date)\
                    .where(Forecast.city == city.upper())\
                    .order_by(Forecast.forecast_date.desc())
                result = await session.execute(stmt)
                forecast_data = result.first()
                if forecast_data:
                    return jsonify(tuple(forecast_data)), 200
                else:
                    return {"error": f"no data for {usrdate}"}, 200
    except TypeError as e:
        return {"error": f"Malformed data: {e}"},  400


@app.route('/weather/<city>/<usrdate>', methods=['GET'])
async def get_weather(city, usrdate):
    '''
        Example Query:
        SELECT * FROM (measurement M 
        JOIN
            (SELECT station.code as station, sensor.id as sensor_id 
            FROM public.station JOIN sensor
            ON station.code = sensor.station_code) as S
        ON M.station = S.station and M.sensor_id = S.sensor_id) as Res
        WHERE Res.date::date = date '2024-05-28' 
    '''
    try:
        target_date = date.fromisoformat(escape(usrdate))
        async with async_session() as session:
            async with session.begin():
                subq = select(Station, Sensor).join(Sensor).subquery()
                station_subq = aliased(Station, subq, name="station")
                sensor_subq = aliased(Sensor, subq, name="sensor")
                #stmt = select(Measurement, station_subq, sensor_subq)\
                stmt = select(Measurement)\
                .join(subq, Measurement.station == station_subq.code and Measurement.sensor_id == sensor_subq.sensor_id)\
                .where(cast(Measurement.date, Date) == target_date)
                result = await session.execute(stmt)
                data = result.fetchall()
                return calc_averages(data=data, city=city, date=usrdate), 200
    except TypeError as e:
        return {"error": f"Malformed data: {e}"},  400


@app.route('/station', methods=['POST'])
async def add_station():
    '''Adds a new meteorological station'''
    try:
        S = Station(**request.json)
        async with async_session() as session:
            async with session.begin():
                session.add(S)
                return jsonify(S), 201
    except TypeError as e:
        return {"error": f"Malformed data: {e}"},  400
    except IntegrityError as e:
        return {"error": f"Integrity Error: {e}"},  400


@app.route('/station', methods=['PUT'])
async def replace_station():
    '''Replaces (edits) a meteorological station'''
    try:
        S = Station(**request.json)
        async with async_session() as session:
            async with session.begin():
                stmt = update(Station)\
                .where(Station.code == S.code)\
                .values(city=S.city, latitude=S.latitude,
                        longtitude=S.longtitude, date_install=S.date_install)
                await session.execute(stmt)
                return jsonify(S), 201
    except TypeError as e:
        return {"error": f"Malformed data: {e}"},  400
    except IntegrityError as e:
        return {"error": f"Integrity Error: {e}"},  400


@app.route('/station/<code>', methods=['DELETE'])
async def delete_station(code):
    '''Deletes the meteorological station with code: code'''
    try:
        async with async_session() as session:
            async with session.begin():
                stmt = delete(Station)\
                .where(Station.code == code)
                await session.execute(stmt)
                return 200
    except IntegrityError as e:
        return {"error": f"Integrity Error: {e}"},  400


@app.route('/sensor', methods=['POST'])
async def add_sensor():
    try:
        S = Sensor(**request.json)
        async with async_session() as session:
            async with session.begin():
                session.add(S)
                return jsonify(S), 201
    except TypeError as e:
        return {"error": f"Malformed data: {e}"},  400
    except IntegrityError as e:
        return {"error": f"Integrity Error: {e}"},  400

