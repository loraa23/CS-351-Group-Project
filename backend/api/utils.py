from icalendar import Calendar
from datetime import datetime, date
import re


DUMMY_WEEK = {
    "MO": date(2025, 1, 6),
    "TU": date(2025, 1, 7),
    "WE": date(2025, 1, 8),
    "TH": date(2025, 1, 9),
    "FR": date(2025, 1, 10),
    "SA": date(2025, 1, 11),
    "SU": date(2025, 1, 12),
}

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
                    "original_start": dtstart.isoformat(),
                    "original_end": dtend.isoformat(),

                    # generic weekly display date-times
                    "display_start": display_start.isoformat(),
                    "display_end": display_end.isoformat(),
                })

    return events

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
