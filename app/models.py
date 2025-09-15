import enum
from uuid import uuid4, UUID
from dataclasses import dataclass
from sqlalchemy.types import TIMESTAMP
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import date


@dataclass
class Measurement(db.Model):
    __tablename__ = "measurement"
    measurement_id: so.Mapped[str] = so.mapped_column(sa.String(64))
    station: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    sensor_id: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                 primary_key=True)
    date: so.Mapped[TIMESTAMP] = so.mapped_column(sa.TIMESTAMP(timezone=True),
                                                  primary_key=True)
    category: so.Mapped[str] = so.mapped_column(sa.String(64))
    measurement: so.Mapped[int] = so.mapped_column(sa.Integer)
    unit: so.Mapped[str] = so.mapped_column(sa.String(64))
 
    def __repr__(self):
        return f"<Measurement {self.measurement_id}>"

@dataclass
class Station(db.Model):
    __tablename__ = "station"
    code: so.Mapped[str] = so.mapped_column(sa.String(64),
                                            primary_key=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    latitude: so.Mapped[float] = so.mapped_column(sa.Float)
    longtitude: so.Mapped[float] = so.mapped_column(sa.Float)
    date_install: so.Mapped[TIMESTAMP] = so.mapped_column(sa.TIMESTAMP)
 
    def __repr__(self):
        return f"<City {self.code} {self.city}>"

@dataclass
class Sensor(db.Model):
    __tablename__ = "sensor"
    id: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                 primary_key=True)
    station_code: so.Mapped[str] = so.mapped_column(sa.ForeignKey("station.code"), index=True)
    category: so.Mapped[str] = so.mapped_column(sa.String(64))
    
    def __repr__(self):
        return f"<Sensor {self.id} {self.station_code} {self.category}>"

@dataclass
class Forecast(db.Model):
    __tablename__ = "forecast"
    forecast_date: so.Mapped[date] = so.mapped_column(sa.Date, primary_key=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64), primary_key=True)
    temperature: so.Mapped[int] = so.mapped_column(sa.Integer)
    humidity: so.Mapped[int] = so.mapped_column(sa.Integer)
    wind: so.Mapped[int] = so.mapped_column(sa.Integer)
 
    def __repr__(self):
        return f"<Forecast {self.date} {self.city} {self.temperature} {self.humidity} {self.wind}>"
