from Transform.filter_status import filter_status
from Transform.add_location import add_location

transform_steps = [
    {"step": "FILTER_STATUS", "function": filter_status},
    {"step": "ADD_LOCATION", "function": add_location},
]
