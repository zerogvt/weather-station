DROP TABLE IF EXISTS measurements;

CREATE TABLE measurements (
    measurement_id UUID PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    time TIMESTAMPTZ NOT NULL,
    station TEXT NOT NULL,
    category TEXT NOT NULL,
    measurement DOUBLE PRECISION NOT NULL,
    unit TEXT NOT NULL,
);