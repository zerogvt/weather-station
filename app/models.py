from uuid import uuid4, UUID
from dataclasses import dataclass
from sqlalchemy.types import TIMESTAMP
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


@dataclass
class Measurement(db.Model):
    measurement_id: so.Mapped[UUID] = so.mapped_column(primary_key=True)
    station: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    sensor_id: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    date: so.Mapped[TIMESTAMP] = so.mapped_column(sa.TIMESTAMP)
    category: so.Mapped[str] = so.mapped_column(sa.String(64))
    measurement: so.Mapped[int] = so.mapped_column(sa.Integer)
    unit: so.Mapped[str] = so.mapped_column(sa.String(64))
 

    def __repr__(self):
        return f"<Measurement {self.measurement_id}>"
