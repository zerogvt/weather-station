from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
engine = create_async_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

migrate = Migrate(app, db)

from app import routes, models
