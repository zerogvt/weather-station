from app import app, async_session
from app.utils import flatten_data
from app.models import Measurement
from flask import jsonify, request
from sqlalchemy.sql import select
from sqlalchemy.exc import IntegrityError


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
        return {"error": f"Malformed measurement: {e}"},  400
    except IntegrityError as e:
        return {"error": f"Integrity Error: {e}"},  400
