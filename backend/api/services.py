from .models import Event
from .rbtree import RedBlackTree
from .unionfind import UnionFind

rbtree = RedBlackTree() # Shared tree to store events

# Creates event and inserts into tree
# def add_event(title, start_time, end_time, campus="", building="", room="",days=""):
#     event = Event.objects.create(
#         title=title,
#         start_time=start_time,
#         end_time=end_time,
#         campus=campus,
#         building=building,
#         room=room,
#         days=days
#     )
#     rbtree.insert(event)
#     return event

# Returns events in time order
def get_ordered_events():
    return rbtree.inorder()

# added for second data structure
def group_similar_schedules(schedule_list):
    uf = UnionFind(len(schedule_list))
    for i in range(len(schedule_list)):
        for j in range(i + 1, len(schedule_list)):
            set_i = set(schedule_list[i])
            set_j = set(schedule_list[j])
            if set_i & set_j:
                uf.union(i, j)
    return uf