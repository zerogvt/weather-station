# weather-station
Meteorological WEB App Ingesting IoT Weather Station Data

# Example http calls
See populate_db.sh

# Docker
## Build
`docker build -t zerogvt/weather .`

## Run
`docker run -it -v ${PWD}/pgdata:/weather/pgdata -p 5000:5000 --network="host" zerogvt/weather` 
