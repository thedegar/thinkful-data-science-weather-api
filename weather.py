#####################################################
# Tyler Hedegard
# 6/20/2016
# Thinkful Data Science
# Weather API
#####################################################

import datetime
import requests
import sqlite3 as lite
import pandas as pd


# Connect to the database
con = lite.connect('weather.db')

# Data for API
cities = {
    "Atlanta": '33.762909,-84.422675',
    "Austin": '30.303936,-97.754355',
    "Boston": '42.331960,-71.020173',
    "Chicago": '41.837551,-87.681844',
    "Cleveland": '41.478462,-81.679435'
    }
        
cities_tup = tuple(cities.iteritems())

key = 'f62d357ad457ae6460a6f2c3b9091653'
dt = datetime.datetime.now()
days = 30
start_date = dt - datetime.timedelta(days=days)
ts = dt.strftime('%Y-%m-%dT%H:%M:%S')

with con:
    cur = con.cursor()
    # Create the cities and weather tables
    cur.execute("DROP TABLE IF EXISTS temp")
    cur.execute("DROP TABLE IF EXISTS cities")
    cur.execute("CREATE TABLE temp (city text, date text, max_temp float)")
    cur.execute("CREATE TABLE cities (city text, coordinates text)")
    
    cur.executemany("INSERT INTO cities VALUES(?,?)", cities_tup)

    for each in cities:
        for day in range(1,days+1):
            date = dt - datetime.timedelta(days=day)
            ts = date.strftime('%Y-%m-%dT%H:%M:%S')
            api = 'https://api.forecast.io/forecast/'+key+'/'+cities[each]+','+ts
            city = each
            r = requests.get(api)
            temp = r.json()['daily']['data'][0]['temperatureMax']
            data = (city, ts, temp)
            cur.execute("INSERT INTO temp VALUES(?,?,?)", data)

    cur.execute("SELECT * FROM temp")
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=cols)

for each in cities:
    condition = (df['city'] == each)
    data = df[condition]['max_temp']
    avg = data.mean()
    min = data.min()
    max = data.max()
    range = max - min
    var = data.var()
    print("For {} the descriptive statistics are: ".format(each))
    print("  Mean = {}".format(avg))
    print("  Range = {}".format(range))
    print("  Variance = {}".format(var))
