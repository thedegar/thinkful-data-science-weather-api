#####################################################
# Tyler Hedegard
# 6/20/2016
# Thinkful Data Science
# Weather API
#####################################################

import datetime
import requests

cities = {"Atlanta": '33.762909,-84.422675',
          "Austin": '30.303936,-97.754355',
          "Boston": '42.331960,-71.020173',
          "Chicago": '41.837551,-87.681844',
          "Cleveland": '41.478462,-81.679435'
          }

key = 'f62d357ad457ae6460a6f2c3b9091653'
dt = datetime.datetime.now()
start_date = dt - datetime.timedelta(days=30)
ts = dt.strftime('%Y-%m-%dT%H:%M:%S')

api = 'https://api.forecast.io/forecast/'+key+'/'+cities['Austin']+','+ts

r = requests.get(api)
