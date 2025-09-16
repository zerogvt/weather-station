from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate
from sqlalchemy import text

async def convert_measurement_to_hypertable(session):
    '''
    Convert measurement table to a hypertable 
    https://docs.tigerdata.com/api/latest/hypertable/create_hypertable/
    '''
    async with session as ses:
        stmt = text(f"""
                    SELECT create_hypertable('measurement', \
                    by_range('date', INTERVAL '1 day'), \
                    if_not_exists => TRUE);
                    """)
        await ses.execute(stmt)



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
engine = create_async_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

migrate = Migrate(app, db)

convert_measurement_to_hypertable(async_session)

from app import routes, models

