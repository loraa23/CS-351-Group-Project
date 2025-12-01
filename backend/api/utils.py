from icalendar import Calendar
from datetime import datetime, date, timedelta, time
from .rbtree import RedBlackTree
from .metra import find_morning_commute, find_evening_commute
from .unionFind import UnionFind
from .models import Enrollment, Course, Availability, Student
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

# extracts courses from a list of events and adds each course to Course model
# updates Enrollment model
def extract_courses_from_events(student, events):

    for event in events:
        title = event["title"] 

        # extract course code 
        match = re.search(r"[A-Z]{2,4}\s?\d{2,3}", title)
        if not match:
            continue  # skip non-class events
        course_code = match.group().replace(" ", "")

        # create new course object
        course, created = Course.objects.get_or_create(
            course_code=course_code,
            defaults={"course_name": title},
        )

        Enrollment.objects.get_or_create(student=student, course=course)

# extracts free time from student schedule given list of events (classes + commute)
# Note: assumes there are no overlapping classes or commutes
def extract_availability_from_events(student, events):
    WEEKDAY_MAP = {"MO": 0, "TU":1, "WE":2, "TH":3, "FR":4, "SA":5, "SU":6}
    # group class blocks by weekday
    day_blocks = {d: [] for d in WEEKDAY_MAP}

    for event in events:
        start = datetime.fromisoformat(event['display_start']).time()
        end = datetime.fromisoformat(event['display_end']).time()

        for day in event["days"]:
            day_blocks[day].append((start, end))

    # delete previous availability (refresh)
    Availability.objects.filter(student=student).delete()

    # process each day
    for day_code, blocks in day_blocks.items():
        weekday = WEEKDAY_MAP[day_code]

        if not blocks:
            # whole day free
            Availability.objects.create(
                student=student,
                day_of_week=weekday,
                start_time=time(0,0),
                end_time=time(23,59)
            )
            continue

        # sort class blocks by start time
        blocks.sort()

        free_start = time(0,0)
        for class_start, class_end in blocks:
            if free_start < class_start:
                # free interval before this class
                Availability.objects.create(
                    student=student,
                    day_of_week=weekday,
                    start_time=free_start,
                    end_time=class_start
                )
            # next free_start is after this class
            free_start = class_end

        # last free block until midnight
        if free_start < time(23,59):
            Availability.objects.create(
                student=student,
                day_of_week=weekday,
                start_time=free_start,
                end_time=time(23,59)
            )

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
                    "display_start": start_time.isoformat(),
                    "display_end": end_time.isoformat(),
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
                    "display_start": start_time.isoformat(),
                    "display_end": end_time.isoformat(),
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
    trees = {day: RedBlackTree() for day in WEEKDAYS}

    # insert each event into corresponding rbtree
    for event in events:
        start = datetime.fromisoformat(event['display_start']).time()
        end = datetime.fromisoformat(event['display_end']).time()
        
        for day in event['days']:
            trees[day].insert(start, {"start": start, "end": end}) # using start time as key


    # compute earliest and latest times using inorder traversal
    for day in WEEKDAYS:
        rbt = trees[day]
        sorted_events = rbt.inorder() # sorted by start time

        if len(sorted_events) == 0:
            continue

        # earliest start = first element's start
        bounds[day]["earliest"] = sorted_events[0]["start"]

        # latest end = maximum end-time over all events for that day
        latest = sorted_events[0]["end"]
        for ev in sorted_events:
            if ev["end"] > latest:
                latest = ev["end"]

        bounds[day]["latest"] = latest

    return bounds

# computes the amount of time in minutes for two time blocks
def overlap_in_minutes(a_start, a_end, b_start, b_end):
    latest_start = max(a_start, b_start)
    earliest_end = min(a_end, b_end)
    delta = (datetime.combine(datetime.min, earliest_end) - 
             datetime.combine(datetime.min, latest_start))
    return max(0, delta.total_seconds() / 60)

# given two students s1 and s2, returns a score 
# based on how much their free time overalps (0% = no overlap, 100% overlap)
# TODO: add course overlap to score
def compute_match_score(s1, s2):
    weekly_overlap = 0

    for day in range(0, 5):  # Monday–Friday
        a1 = Availability.objects.filter(student=s1, day_of_week=day)
        a2 = Availability.objects.filter(student=s2, day_of_week=day)

        # compare free time blocks
        overlaps = 0
        for f1 in a1:
            for f2 in a2:
                start = max(f1.start_time, f2.start_time)
                end = min(f1.end_time, f2.end_time)

                if start < end:
                    delta = (
                        timedelta(
                            hours=end.hour, minutes=end.minute
                        ) - timedelta(
                            hours=start.hour, minutes=start.minute
                        )
                    )
                    overlaps += delta.seconds // 60  # minutes

        # daily fraction
        daily_fraction = overlaps / (24 * 60)
        weekly_overlap += daily_fraction

    # normalize to percent
    availability_percent = weekly_overlap / 5 * 100  # 0–100 scale

    return round(availability_percent)

# uses UnionFind to form stduy group clusters of students 
def form_study_groups(threshold=30):
    uf = UnionFind()
    all_students = list(Student.objects.all())

    # initialize sets using user
    for s in all_students:
        uf.make_set(s.user)

    # compare students pairwise and union if score >= threshold
    for i, s1 in enumerate(all_students):
        for s2 in all_students[i+1:]:
            score = compute_match_score(s1, s2)
            if score >= threshold:
                uf.union(s1.user, s2.user)

    # collect groups
    groups = {}
    for s in all_students:
        root_user = uf.find(s.user)
        if root_user not in groups:
            groups[root_user] = []
        groups[root_user].append(s)

    # for debugging, delete later
    print("=== Study Groups ===")
    for root, members in groups.items():
        print(f"\nGroup rooted at {root.username}:")
        for m in members:
            print(f"  - {m.user.username}")

    return groups, uf

# ranks other students within a cluster based on availability overlap
def ranked_matches_within_group(target_student, threshold=30):
    groups, uf = form_study_groups(threshold) # build study groups
    target_root = uf.find(target_student.user)

    # get the cluster target_student is in
    cluster = groups.get(target_root, [])

    matches = [] # list of possible student matches
    for s in cluster:
        if s == target_student:
            continue

        score = compute_match_score(target_student, s)

        if score > 0: # ignore 0% matches
            score = round(score) 
            matches.append((s, score))

    matches.sort(key=lambda x: x[1], reverse=True)

    results = []
    for s, score in matches:
        results.append({
            "username": s.user.username,
            "email": s.email,
            "score": score,
            "schedule_id": s.schedule.id if s.schedule else None,
            "train_line": s.train_line,
            "station": s.station
        })
    
    # for s, score in matches:
    #     print(f"{s.user.username} — {score}%")
    #     matches_string.append(f"{s.user.username} — {score}% match")

    return results



# not currently in use, but could be useful if we need exact class locations
# extracts campus, building, and room number from a location string
# formatted: LOCATION:Campus: X Building: Y Room: Z
# def parse_location(location_str):
#     campus_match = re.search(r'Campus:\s*(.*?)\s*(?=Building:|$)', location_str)
#     building_match = re.search(r'Building:\s*(.*?)\s*(?=Room:|$)', location_str)
#     room_match = re.search(r'Room:\s*(.*)$', location_str)

#     campus = campus_match.group(1).strip() if campus_match else ""
#     building = building_match.group(1).strip() if building_match else ""
#     room = room_match.group(1).strip() if room_match else ""

#     return campus, building, room
