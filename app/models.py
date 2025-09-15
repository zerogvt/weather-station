from uuid import uuid4, UUID
from dataclasses import dataclass
from sqlalchemy.types import TIMESTAMP
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


@dataclass
class Measurement(db.Model):
    #id: so.Mapped[UUID] = so.mapped_column(sa.UUID,primary_key=True,default=uuid4)
    measurement_id: so.Mapped[str] = so.mapped_column(sa.String(64))
    station: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    sensor_id: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                 primary_key=True, index=True)
    date: so.Mapped[TIMESTAMP] = so.mapped_column(sa.TIMESTAMP(timezone=True),
                                                  primary_key=True)
    category: so.Mapped[str] = so.mapped_column(sa.String(64))
    measurement: so.Mapped[int] = so.mapped_column(sa.Integer)
    unit: so.Mapped[str] = so.mapped_column(sa.String(64))
 
    def __repr__(self):
        return f"<Measurement {self.measurement_id}>"

@dataclass
class Station(db.Model):
    code: so.Mapped[str] = so.mapped_column(sa.String(64),
                                            primary_key=True, index=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    latitude: so.Mapped[float] = so.mapped_column(sa.Float)
    longtitude: so.Mapped[float] = so.mapped_column(sa.Float)
    date_install: so.Mapped[TIMESTAMP] = so.mapped_column(sa.TIMESTAMP)
 
    def __repr__(self):
        return f"<City {self.code} {self.city}>"
