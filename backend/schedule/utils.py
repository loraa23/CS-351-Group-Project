from icalendar import Calendar
from .models import Event
import re


# parse ics file and insert information into an Event object
# todo: put event in red-black tree?
def parse_ics(file_path):
    with open(file_path, 'rb') as f:
        cal = Calendar.from_ical(f.read())

        for component in cal.walk():

            # extract each event (class or commute) and create Event object
            if component.name == "VEVENT":
                title = str(component.get('summary'))
                start = component.get('dtstart').dt.time()
                end = component.get('dtend').dt.time()
                location = str(component.get('location', 'Unknown'))
                campus, building, room = parse_location(location)

                rrule = component.get('rrule')
                if rrule and 'BYDAY' in rrule:
                    days = rrule['BYDAY']


                event = Event(title=title, start_time=start, end_time=end, days=days, campus=campus, building=building, room=room)
                event.save()

    return None

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