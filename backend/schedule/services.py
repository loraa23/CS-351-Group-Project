from .models import Event
from .rbtree import RedBlackTree

rbtree = RedBlackTree() # Shared tree to store events

# Creates event and inserts into tree
def add_event(title, start_time, end_time, location="", building="", room=""):
    event = Event.objects.create(
        title=title,
        start_time=start_time,
        end_time=end_time,
        location=location,
        building=building,
        room=room
    )
    rbtree.insert(event)
    return event

# Returns events in time order
def get_ordered_events():
    return rbtree.inorder()
