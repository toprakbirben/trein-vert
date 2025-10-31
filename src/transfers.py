import pandas as pd
import csv

transfers = pd.read_csv("resource/20251027_fahrplaene_gesamtdeutschland_gtfs/transfers.txt")
stops = pd.read_csv("resource/20251027_fahrplaene_gesamtdeutschland_gtfs/stops.txt")

stops_by_station = {}

for _, stop in stops.iterrows():
    station_id = stop['parent_station'] if pd.notna(stop['parent_station']) else stop['stop_id']
    if station_id not in stops_by_station:
        stops_by_station[station_id] = []
    stops_by_station[station_id].append(stop.to_dict()) #make sure to only get stop_id to parent_station

print(stops_by_station)