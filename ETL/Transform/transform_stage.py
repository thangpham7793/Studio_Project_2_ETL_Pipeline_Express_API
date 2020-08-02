from Transform.filter_status import filter_status
from Transform.add_location import add_location
from Transform.filter_columns import filter_columns

transform_steps = [
    {"step": "FILTER_COLUMNS", "function": filter_columns},
    {"step": "FILTER_STATUS", "function": filter_status},
    {"step": "ADD_LOCATION", "function": add_location},
]
