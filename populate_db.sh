#!/bin/bash

# add a station
curl --location 'localhost:5000/station' \
--header 'Content-Type: application/json' \
--data '{
"code": "MET-004",
"city": "ATHENS",
"latitude": 37,
"longtitude": 23,
"date_install": "2024-05-28"
}
'

# add a sensor in above station
curl --location 'localhost:5000/sensor' \
--header 'Content-Type: application/json' \
--data '{
"id": "HUM-001",
"station_code": "MET-004",
"category": "Humidity"
}
'

# add mesurements from above sensor
curl --location 'localhost:5000/ingest' \
--header 'Content-Type: application/json' \
--data '{
"measurement_id": "80d58a78-95d3-4b9c-b0a4-aab2e2ed73d5",
"sensor_id": "HUM-001",
"date": "2024-05-28T15:32:18+02:00",
"station": "MET-004",
"info": {
	"category": "Humidity",
	"measurement": 30,
	"unit": "Percentage"
    }
}
'

curl --location 'localhost:5000/ingest' \
--header 'Content-Type: application/json' \
--data '{
"measurement_id": "80d58a78-95d3-4b9c-b0a4-aab2e2ed73d5",
"sensor_id": "HUM-001",
"date": "2024-05-28T15:42:18+02:00",
"station": "MET-004",
"info": {
	"category": "Humidity",
	"measurement": 40,
	"unit": "Percentage"
    }
}
'
# add a forecast for above city and date
curl --location 'localhost:5000/forecast' \
--header 'Content-Type: application/json' \
--data '{
"forecast_date": "2024-05-28",
"city": "ATHENS",
"temperature": 21,
"humidity": 30,
"wind": 25
}
'

# get forecast for above city/date
curl --location 'localhost:5000/forecast/athens/2024-05-28' \
--header 'Content-Type: application/json'

# get actual weather for above city/date
curl --location 'localhost:5000/weather/athens/2024-05-28' \
--header 'Content-Type: application/json'
