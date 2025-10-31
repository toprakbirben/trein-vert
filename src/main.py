#pip install requests beautifulsoup4 gtfs-realtime-bindings

from google.transit import gtfs_realtime_pb2
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import threading
import pandas as pd


URL_ZUG = "https://www.zugfinder.net/en/stationboard-Amsterdam_Centraal"
feed = gtfs_realtime_pb2.FeedMessage()


#not needed for now, used for web scraping
page = requests.get(URL_ZUG)
soup = BeautifulSoup(page.content, "html.parser")

URL_PB = "https://realtime.gtfs.de/realtime-free.pb"

gtfs_calendar_trips_path = "resource/latest/trips.txt"
gtfs_calendar_routes_path = "resource/latest/routes.txt"

trips = pd.read_csv(gtfs_calendar_trips_path, dtype=str)
routes = pd.read_csv(gtfs_calendar_routes_path, dtype=str)

trips['route_id'] = trips['route_id'].str.strip()
routes['route_id'] = routes['route_id'].str.strip()
routes = routes.drop_duplicates(subset=['route_id'])

merged = trips.merge(routes[['route_id', 'route_short_name']], on='route_id', how='left')

trip_to_route_map = dict(zip(merged['trip_id'], merged['route_short_name']))


def printit():
   threading.Timer(10.0, printit).start() #gtfs data is updated every 10 second, uncomment to get live feed.

   response = requests.get(URL_PB)
   feed.ParseFromString(response.content)

   for entity in feed.entity:
      if entity.HasField('trip_update'):
         trip_update = entity.trip_update
         trip_id = trip_update.trip.trip_id

         for stop_update in trip_update.stop_time_update:
            if stop_update.arrival.delay >= 3600 and stop_update.arrival.delay <= 7200: #can also be negative for early arrival/departure
               route_name = trip_to_route_map.get(trip_id, "N/A")
               #if(route_name != "N/A"):
               print(f"Trip {route_name} {trip_id} arrival is delayed by {stop_update.arrival.delay} seconds")
                  #print()

      


            
printit()


