# weather-station
Meteorological WEB App Ingesting IoT Weather Station Data

# Example http calls
See populate_db.sh

# How to Run
## Build Weather app docker image
`docker build -t zerogvt/weather .`

## Run Postgres with Timescale docker image
(Prior to running:
* create a folder `pgdata` and chown it to `1000`
`mkdir pgdata && sudo chown 1000:1000 pgdata`

* Pull Timescale image `docker pull timescale/timescaledb:latest-pg17`)

`docker run -d --name timescaledb -p 5432:5432  -v./pgdata:/pgdata -e PGDATA=/pgdata -e POSTGRES_PASSWORD=password timescale/timescaledb-ha:pg17`

## Run Weather app
`docker run -it -v ${PWD}/pgdata:/weather/pgdata -p 5000:5000 --network="host" zerogvt/weather`

