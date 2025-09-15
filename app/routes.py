from app import app, async_session
from app.utils import flatten_data
from app.models import Measurement, Forecast, Station, Sensor
from flask import jsonify, request
from sqlalchemy.sql import select
from sqlalchemy.exc import IntegrityError
from datetime import date
from markupsafe import escape


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

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
                # and get actual averages
                

                if forecast_data:
                    return jsonify(tuple(forecast_data)), 200
                else:
                    return {"error": f"no data for {usrdate}"}, 200
    except TypeError as e:
        return {"error": f"Malformed data: {e}"},  400


@app.route('/station', methods=['POST'])
async def add_station():
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

