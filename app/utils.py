
'''
Utility functionality
'''
def flatten_data(y):
    '''
    Flattens a nested JSON object.
    E.g. 
    {
        "measurement_id": "88d58a78-95d3-4b9c-b0a4-aab2e2ed73d5",
        "sensor_id": "HUM-001",
        "date": "2024-05-28T15:22:18+02:00",
        "station": "MET-004",
        "info": {
            "category": "Humidity",
            "measurement": 40,
            "unit": "Percentage"
        }
    }

    becomes

    {
        "measurement_id": "88d58a78-95d3-4b9c-b0a4-aab2e2ed73d5",
        "sensor_id": "HUM-001",
        "date": "2024-05-28T15:22:18+02:00",
        "station": "MET-004",            
        "category": "Humidity",
        "measurement": 40,
        "unit": "Percentage"
    }
    '''
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], a)
        else:
            out[name] = x
    flatten(y)
    return out


def calc_averages(data, date, city):
    '''
    Iterate over Measurement rows and calculate averages for 
    Temperature, Humidity, Wind

    Note: IRL we should check the measurement unit as well and make
    adjustements in case it is not uniform.
    '''
    temp = 0
    temp_n = 0
    hum = 0
    hum_n = 0
    wind = 0
    wind_n = 0
    for row in data:
        print(type(row))
        m = dict(row._mapping)["Measurement"]
        if m.category == "Temperature":
            temp += m.measurement
            temp_n += 1
        elif m.category == "Humidity":
            hum += m.measurement
            hum_n += 1
        elif m.category == "Wind":
            wind += m.measurement
            wind_n_n += 1
    return {"date": date,
            "city": city,
            "temperature": int(temp/temp_n) if temp_n else "na",
            "humidity": int(hum/hum_n) if hum_n else "na",
            "wind": int(wind/wind_n) if wind_n else "na"
            }
