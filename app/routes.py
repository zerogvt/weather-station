'''
flask routes
'''
from app import app, async_session
from app.utils import flatten_data, calc_averages
from app.models import Measurement, Forecast, Station, Sensor
from flask import jsonify, request
from sqlalchemy.sql import select, update, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import date
from markupsafe import escape
from sqlalchemy.orm import aliased, Session
from sqlalchemy import and_, cast, Date


@app.route('/ingest', methods=['POST'])
async def ingest_data():
    '''
    Endpoint where IoT devices will post their data
    '''
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
    except SQLAlchemyError as e:
        return {"error": f"Execution failed: {e}"}, 500


@app.route('/forecast', methods=['POST'])
async def add_forecast():
    '''
    Endpoint where UI will post the forecasts
    '''
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
    except SQLAlchemyError as e:
        return {"error": f"Execution failed: {e}"}, 500


@app.route('/forecast/<city>/<usrdate>', methods=['GET'])
async def get_forecast(city, usrdate):
    '''
    Get the latest forecast for a certain city on a certain date.
    date must be a string in  ISO 8601 format. e.g. "2024-05-28"
    '''
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
    except SQLAlchemyError as e:
        return {"error": f"Execution failed: {e}"}, 500


@app.route('/weather/<city>/<usrdate>', methods=['GET'])
async def get_weather(city, usrdate):
    '''
        Get the real weather (as contrasted to the forecast).
        Returns the average Temperature, Humidity, Wind 
        for a city on a certain date.
        
        date selects a certain window on table measurement 
        (which is to be implemented with TimescaleDB postgres
        extension so as to be efficient)
        On that window we need to select only the sensors belonging to 
        stations that are located in the said city, thus
        we need to join sensor and station and then join the result to 
        the previously selected measurement rows.

        Example Query (pg SQL):
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
                stmt = select(Measurement)\
                .join(subq, Measurement.station == station_subq.code and Measurement.sensor_id == sensor_subq.sensor_id)\
                .where(cast(Measurement.date, Date) == target_date)
                result = await session.execute(stmt)
                data = result.fetchall()
                # once we have all relevant rows we need to calculate
                # averages for temperature, humidity, wind
                return calc_averages(data=data, city=city, date=usrdate), 200
    except TypeError as e:
        return {"error": f"Malformed data: {e}"},  400
    except SQLAlchemyError as e:
        return {"error": f"Execution failed: {e}"}, 500


@app.route('/station', methods=['POST'])
async def add_station():
    '''Endpoint to add a new meteorological station'''
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
    except SQLAlchemyError as e:
        return {"error": f"Execution failed: {e}"}, 500


@app.route('/station', methods=['PUT'])
async def replace_station():
    '''Endpoint to replaces (edit) a meteorological station'''
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
    except SQLAlchemyError as e:
        return {"error": f"Execution failed: {e}"}, 500


@app.route('/station/<code>', methods=['DELETE'])
async def delete_station(code):
    '''Deletes the meteorological station with code: code'''
    try:
        async with async_session() as session:
            async with session.begin():
                stmt = delete(Station)\
                .where(Station.code == code)
                await session.execute(stmt)
                return {}, 200
    except IntegrityError as e:
        return {"error": f"Integrity Error: {e}"},  400
    except SQLAlchemyError as e:
        return {"error": f"Execution failed: {e}"}, 500


@app.route('/sensor', methods=['POST'])
async def add_sensor():
    '''
    Adds a new sensor
    '''
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
    except SQLAlchemyError as e:
        return {"error": f"Execution failed: {e}"}, 500


@app.route('/')
@app.route('/health')
def index():
    '''
    Show if we're up and listening
    '''
    return "up", 200


@app.route('/measurements')
async def get_data():
    '''
    Get all measurements.
    Just for quick tests during dev
    '''
    async with async_session() as session:
        stmt = select(Measurement).order_by(Measurement.date)
        result = await session.execute(stmt)
        data = result.fetchall()
        return jsonify([tuple(row) for row in data])

