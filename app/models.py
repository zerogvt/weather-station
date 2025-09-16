'''
SQLAlchemy models for the weather database
'''
from dataclasses import dataclass
from sqlalchemy.types import TIMESTAMP
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import date


@dataclass
class Station(db.Model):
    '''
    The central entity is a "station".
    A station may have many "sensors" (relationship Sensor).
    A station may produce many "measurements" (relationship Measurement)
    '''
    __tablename__ = "station"
    code: so.Mapped[str] = so.mapped_column(sa.String(64),
                                            primary_key=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    latitude: so.Mapped[float] = so.mapped_column(sa.Float)
    longtitude: so.Mapped[float] = so.mapped_column(sa.Float)
    date_install: so.Mapped[TIMESTAMP] = so.mapped_column(sa.TIMESTAMP)
    
    sensors = so.relationship(
        "Sensor",
        cascade="all, delete",
        backref="station_sensors",
    )

    measurements = so.relationship(
        "Measurement",
        cascade="all, delete",
        backref="station_measurements",
    )


    def __repr__(self):
        return f"<City {self.code} {self.city}>"


@dataclass
class Measurement(db.Model):
    '''
    "measurement" hosts the actual measurements.
    primary key is a composite by a sensor_id and a date 
    so that we protect DB from erroneous floods of the same measurement 
    (note: this is not a DDoS protection as it only protects the DB)

    Each measurement comes for a specific sensor in a specific station,
    thus the foreign keys to them.
    '''
    __tablename__ = "measurement"
    measurement_id: so.Mapped[str] = so.mapped_column(sa.String(64))
    station: so.Mapped[str] = so.mapped_column(sa.ForeignKey("station.code",
                                                             ondelete="CASCADE"),
                                               index=True)
    sensor_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey("sensor.id",
                                                               ondelete="CASCADE"),
                                                 primary_key=True)
    date: so.Mapped[TIMESTAMP] = so.mapped_column(sa.TIMESTAMP(timezone=True),
                                                  primary_key=True)
    category: so.Mapped[str] = so.mapped_column(sa.String(64))
    measurement: so.Mapped[int] = so.mapped_column(sa.Integer)
    unit: so.Mapped[str] = so.mapped_column(sa.String(64))
 
    def __repr__(self):
        return f"<Measurement {self.measurement_id}>"
    

@dataclass
class Sensor(db.Model):
    '''
    "sensor" hosts all the sensors.
    Each sensor belongs to a specific "station", thus the foreign key to it.
    '''
    __tablename__ = "sensor"
    id: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                 primary_key=True)
    station_code: so.Mapped[str] = so.mapped_column(sa.ForeignKey("station.code",
                                                                  ondelete="CASCADE"))
    category: so.Mapped[str] = so.mapped_column(sa.String(64))

    measurements = so.relationship(
        "Measurement",
        cascade="all, delete",
        backref="sensor_measurements",
    )
    def __repr__(self):
        return f"<Sensor {self.id} {self.station_code} {self.category}>"

@dataclass
class Forecast(db.Model):
    '''
    "forecast" hosts the forecasts that users enter in the system.
    '''
    __tablename__ = "forecast"
    forecast_date: so.Mapped[date] = so.mapped_column(sa.Date, primary_key=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64), primary_key=True)
    temperature: so.Mapped[int] = so.mapped_column(sa.Integer)
    humidity: so.Mapped[int] = so.mapped_column(sa.Integer)
    wind: so.Mapped[int] = so.mapped_column(sa.Integer)
 
    def __repr__(self):
        return f"<Forecast {self.date} {self.city} {self.temperature} {self.humidity} {self.wind}>"
