from app import app, async_session
from app.models import Measurement
from flask import jsonify
from sqlalchemy.sql import select


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/async-data')
async def get_data():
    async with async_session() as session:
        stmt = select(Measurement).order_by(Measurement.date)
        result = await session.execute(stmt)
        data = result.fetchall()
        return jsonify([tuple(row) for row in data])
