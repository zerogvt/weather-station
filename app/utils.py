
def flatten_data(y):
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