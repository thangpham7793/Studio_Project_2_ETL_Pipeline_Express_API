from Util import Util

from Extract.read_file import read_file
from Extract.basic_clean_up import basic_clean_up
from Extract.validate_colnames import validate_colnames
from Transform.filter_columns import filter_columns

steps = [
    {"step": "READ_FILE", "function": read_file},
    {"step": "VALIDATE_COLNAMES", "function": validate_colnames},
    {"step": "BASIC_CLEAN_UP", "function": basic_clean_up},
    {"step": "FILTER_COLUMNS", "function": filter_columns},
]

file_path = "./data/texas_mines_data.xlsx"

run_pipeline = Util.make_pipeline(file_path, steps)
run_pipeline()
