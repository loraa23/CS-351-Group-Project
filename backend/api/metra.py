import os
import io
import zipfile
import requests
import pandas as pd
from datetime import datetime, time, timedelta
from rest_framework.response import Response

STATIC_GTFS_URL = "https://schedules.metrarail.com/gtfs/schedule.zip"
STATIC_GTFS_DIR = "metra_gtfs"

# download gts data if missing
def download_static_gtfs():
    if not os.path.exists(STATIC_GTFS_DIR):
        os.makedirs(STATIC_GTFS_DIR)

    # Download only if files are missing
    required = ["stops.txt", "stop_times.txt", "routes.txt", "trips.txt", "calendar.txt"]
    if all(os.path.exists(os.path.join(STATIC_GTFS_DIR, f)) for f in required):
        return

    response = requests.get(STATIC_GTFS_URL)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(STATIC_GTFS_DIR)

# csv file cleanup
def read_gtfs_file(fname):
    df = pd.read_csv(fname, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    return df

# load all GTS file once
_stops = None
_stop_times = None
_trips = None
_routes = None
_calendar = None

def load_gtfs():
    global _stops, _stop_times, _trips, _routes, _calendar

    if _stops is None:
        download_static_gtfs()
        _stops = read_gtfs_file(os.path.join(STATIC_GTFS_DIR, "stops.txt"))
        _stop_times = read_gtfs_file(os.path.join(STATIC_GTFS_DIR, "stop_times.txt"))
        _trips = read_gtfs_file(os.path.join(STATIC_GTFS_DIR, "trips.txt"))
        _routes = read_gtfs_file(os.path.join(STATIC_GTFS_DIR, "routes.txt"))
        _calendar = read_gtfs_file(os.path.join(STATIC_GTFS_DIR, "calendar.txt"))

    return _stops, _stop_times, _trips, _routes, _calendar

def parse_gtfs_time(gtfs_str):
    """Convert 'HH:MM:SS' (can exceed 24h) into datetime.time"""
    if pd.isna(gtfs_str):
        return None

    h, m, s = map(int, gtfs_str.split(":"))
    h = h % 24  # Handle 24:xx or 25:xx next-day times
    try:
        return time(hour=h, minute=m, second=s)
    except Exception as e:
         return Response(
                {"error": f"Failed to parse schedule: {e}"},
                status=500
            )

ICS_DAY_TO_GTFS = {
    "MO": "monday",
    "TU": "tuesday",
    "WE": "wednesday",
    "TH": "thursday",
    "FR": "friday",
    "SA": "saturday",
    "SU": "sunday",
}

def get_valid_service_ids_for_day(calendar, weekday):
    return calendar[calendar[weekday] == 1]["service_id"].unique()

def get_stations_for_route(route_id):
    stops, stop_times, trips, routes, calendar = load_gtfs()

    route_trips = trips[trips.route_id == route_id]
    if route_trips.empty:
        return []

    merged = stop_times.merge(route_trips, on="trip_id")
    stop_ids = merged["stop_id"].unique()

    stations = stops[stops.stop_id.isin(stop_ids)]
    return sorted(stations.stop_name.unique().tolist())

# determines city endpoint station based on line 
# ex: (MDW -> Chicago Union Station)
def get_endpoint_station(route_id):
    stops, stop_times, trips, routes, calendar = load_gtfs()

    toward_school = trips[(trips.route_id == route_id) & (trips.direction_id == 1)]

    if toward_school.empty:
        return None

    return toward_school.trip_headsign.mode().iloc[0]

def get_route_stop_times(route_id):
    stops, stop_times, trips, routes, calendar = load_gtfs()

    route_trips = trips[trips.route_id == route_id]
    route_stop_times = stop_times.merge(route_trips, on="trip_id")

    return route_stop_times, stops, trips, calendar

# returns the latest morning train based on earliest class start time
def find_morning_commute(route_id, home_station, class_start_time, day):
    stop_times, stops, trips, calendar = get_route_stop_times(route_id)

    weekday = ICS_DAY_TO_GTFS[day]
    valid_services = get_valid_service_ids_for_day(calendar, weekday)

    valid_trips = trips[
        (trips.route_id == route_id) &
        (trips.direction_id == 1) &
        (trips.service_id.isin(valid_services))
    ]

    if valid_trips.empty:
        return None

    valid_trip_ids = valid_trips.trip_id.unique()
    route_stop_times = stop_times[stop_times.trip_id.isin(valid_trip_ids)]

    endpoint = get_endpoint_station(route_id)
    home_stop_id = stops.loc[stops.stop_name == home_station, "stop_id"].values[0]
    endpoint_stop_id = stops.loc[stops.stop_name == endpoint, "stop_id"].values[0]

    home_times = route_stop_times[route_stop_times.stop_id == home_stop_id].copy()
    endpoint_times = route_stop_times[route_stop_times.stop_id == endpoint_stop_id].copy()

    merged = home_times.merge(endpoint_times, on="trip_id", suffixes=("_home", "_endpoint"))

    merged["arrival_time_endpoint"] = merged["arrival_time_endpoint"].apply(parse_gtfs_time)
    merged["departure_time_home"] = merged["departure_time_home"].apply(parse_gtfs_time)

    possible = merged[merged["arrival_time_endpoint"] <= class_start_time]

    if possible.empty:
        return None

    best = possible.sort_values("arrival_time_endpoint").iloc[-1]

    return {
        "departure_time": best["departure_time_home"],
        "arrival_time": best["arrival_time_endpoint"],
        "home_station": home_station,
        "endpoint_station": endpoint,
        "trip_id": best["trip_id"]
    }

# finds the earliest evening train based on latest class end time
def find_evening_commute(route_id, home_station, class_end_time, day):
    stop_times, stops, trips, calendar = get_route_stop_times(route_id)

    weekday = ICS_DAY_TO_GTFS[day]
    valid_services = get_valid_service_ids_for_day(calendar, weekday)

    valid_trips = trips[
        (trips.route_id == route_id) &
        (trips.direction_id == 0) &
        (trips.service_id.isin(valid_services))
    ]

    if valid_trips.empty:
        return None

    valid_trip_ids = valid_trips.trip_id.unique()
    route_stop_times = stop_times[stop_times.trip_id.isin(valid_trip_ids)]

    endpoint = get_endpoint_station(route_id)
    home_stop_id = stops.loc[stops.stop_name == home_station, "stop_id"].values[0]
    endpoint_stop_id = stops.loc[stops.stop_name == endpoint, "stop_id"].values[0]

    endpoint_times = route_stop_times[route_stop_times.stop_id == endpoint_stop_id].copy()
    home_times = route_stop_times[route_stop_times.stop_id == home_stop_id].copy()

    merged = endpoint_times.merge(home_times, on="trip_id", suffixes=("_endpoint", "_home"))

    merged["departure_time_endpoint"] = merged["departure_time_endpoint"].apply(parse_gtfs_time)
    merged["arrival_time_home"] = merged["arrival_time_home"].apply(parse_gtfs_time)

    possible = merged[merged["departure_time_endpoint"] >= class_end_time]

    if possible.empty:
        return None

    best = possible.sort_values("departure_time_endpoint").iloc[0]

    return {
        "departure_time": best["departure_time_endpoint"],
        "arrival_time": best["arrival_time_home"],
        "home_station": home_station,
        "endpoint_station": endpoint,
        "trip_id": best["trip_id"]
    }

# returns list of stations on a given Metra line 
# ex: (MDW -> [Big Timber, Elgin, ...])
def get_stations_for_route(route_id):
    stops, stop_times, trips, routes, calendar = load_gtfs()

    route_trips = trips[trips["route_id"] == route_id]

    if route_trips.empty:
        return []
    
    # Pick any trip (all trips on a route share the same stops, only times differ)
    some_trip_id = route_trips.iloc[0]["trip_id"]
   

    # Get all stop_ids for this trip
    trip_stops = stop_times[stop_times["trip_id"] == some_trip_id]

    # Merge with stops.txt to get names
    merged = trip_stops.merge(stops, on="stop_id")

    # Sort by stop_sequence so they appear in correct travel order
    merged = merged.sort_values("stop_sequence")

    # Return the station names
    return merged["stop_name"].tolist()
