from icalendar import Calendar
from datetime import datetime, date, timedelta
from .rbtree import RedBlackTree
from .metra import find_morning_commute, find_evening_commute
import os
import re

WEEKDAYS = ["MO", "TU", "WE", "TH", "FR"]

# used to create a generic weekly view for 
# react big calendar
DUMMY_WEEK = { 
    "MO": date(2025, 1, 6),
    "TU": date(2025, 1, 7),
    "WE": date(2025, 1, 8),
    "TH": date(2025, 1, 9),
    "FR": date(2025, 1, 10),
    "SA": date(2025, 1, 11),
    "SU": date(2025, 1, 12),
}

# parses a UIC .ics file and returns a list of dictionary events
def parse_ics(file_path):
    events = []

    with open(file_path, "rb") as f:
        cal = Calendar.from_ical(f.read())

        for comp in cal.walk():

            if comp.name != "VEVENT":
                continue

            summary = str(comp.get("summary"))

            dtstart = comp.get("dtstart").dt  # real datetime
            dtend = comp.get("dtend").dt

            start_time = dtstart.time()
            end_time = dtend.time()

            # Recurrence rule
            rrule = comp.get("rrule")
            if rrule and "BYDAY" in rrule:
                days = rrule["BYDAY"]  # e.g., ["MO","WE","FR"]
            else:
                # One-off event: derive weekday
                weekday = dtstart.strftime("%a").upper()[:2]
                days = [weekday]

            location = str(comp.get("location", "Unknown"))

            # Create separate events per day
            for day_code in days:
                dummy_date = DUMMY_WEEK[day_code]

                # datetime used for front-end
                display_start = datetime.combine(dummy_date, start_time)
                display_end = datetime.combine(dummy_date, end_time)

                events.append({
                    "title": summary,
                    "days": days,
                    "location": location,

                    # real ICS date-times preserved
                    # "original_start": dtstart.isoformat(),
                    # "original_end": dtend.isoformat(),

                    # generic weekly display date-times
                    "display_start": display_start.isoformat(),
                    "display_end": display_end.isoformat(),
                    "type": "class"
                })

    return events

# subtracts or adds X number of minutes to datetime object
def shift_time(t: datetime.time, minutes: int) -> datetime.time:
    """
    Shift a datetime.time object by +/- minutes and return a new time.
    Negative minutes = subtract.
    """
    dummy_date = datetime(2000, 1, 1, t.hour, t.minute, t.second)
    shifted = dummy_date + timedelta(minutes=minutes)
    return shifted.time()

def generate_commute_schedule(file_path, train_line, station):

    events = parse_ics(file_path)
    bounds = compute_class_bounds(events)

    # add commutes to list of events
    try: 
        for day in WEEKDAYS:
            dummy_date = DUMMY_WEEK[day]

            # add 20 minute buffer to account for commute between train station and school
            morning_time = shift_time(bounds[day]["earliest"], -20)   # subtract 20 minutes 
            evening_time = shift_time(bounds[day]["latest"], +20)     # add 20 minutes

            if morning_time: # there is class on this day
                commute = find_morning_commute(train_line, station, morning_time, day)
                start_time = datetime.combine(dummy_date, commute["departure_time"])
                end_time = datetime.combine(dummy_date, commute["arrival_time"])
                events.append({
                    "title": f"Metra {train_line} Commute",
                    "display_start": start_time,
                    "display_end": end_time,
                    "days": [day],
                    "location": f"{station} → {commute['endpoint_station']}",
                    "type": "commute"
                })
            
            if evening_time:
                commute = find_evening_commute(train_line, station, evening_time, day)
                start_time = datetime.combine(dummy_date, commute["departure_time"])
                end_time = datetime.combine(dummy_date, commute["arrival_time"])

                events.append({
                    "title": f"Metra {train_line} Commute",
                    "display_start": start_time,
                    "display_end": end_time,
                    "days": [day],
                    "location": f"{commute['endpoint_station']} → {station}",
                    "type": "commute"
                })
    except Exception as e:
        print(e)

    return events 

# finds the earliest start time and latest end time for each day of the week
def compute_class_bounds(events):
    bounds = {day: {"earliest": None, "latest": None} for day in WEEKDAYS}

    for event in events:
        for day in event['days']:

            start = datetime.fromisoformat(event['display_start']).time()
            end = datetime.fromisoformat(event['display_end']).time()

            # earliest start
            if bounds[day]["earliest"] is None or start < bounds[day]["earliest"]:
                bounds[day]["earliest"] = start

            # latest end
            if bounds[day]["latest"] is None or end > bounds[day]["latest"]:
                bounds[day]["latest"] = end

    return bounds


# not currently in use
# extracts campus, building, and room number from a location string
# formatted: LOCATION:Campus: X Building: Y Room: Z
def parse_location(location_str):
    campus_match = re.search(r'Campus:\s*(.*?)\s*(?=Building:|$)', location_str)
    building_match = re.search(r'Building:\s*(.*?)\s*(?=Room:|$)', location_str)
    room_match = re.search(r'Room:\s*(.*)$', location_str)

    campus = campus_match.group(1).strip() if campus_match else ""
    building = building_match.group(1).strip() if building_match else ""
    room = room_match.group(1).strip() if room_match else ""

    return campus, building, room
