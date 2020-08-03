import Util
import pandas as pd

from Extract.read_file import read_file
from Extract.basic_clean_up import basic_clean_up
from Extract.validate_colnames import validate_colnames

from Transform.filter_columns import filter_columns
from Transform.add_location import add_location
from Transform.stringify_rows import stringify_rows
from Transform.filter_rows import filter_rows

from Load.load_into_database import load_into_database

steps = [
    {"step": "READ_FILE", "function": read_file},
    {"step": "VALIDATE_COLNAMES", "function": validate_colnames},
    {"step": "BASIC_CLEAN_UP", "function": basic_clean_up},
    # {"step": "FILTER_COLUMNS", "function": filter_columns},
    {"step": "ADD_LOCATION", "function": add_location},
    {"step": "STRINGIFY_ROWS", "function": stringify_rows},
    # {"step": "LOAD_INTO_DATABASE", "function": load_into_database},
]


def main(file_path):
    run_pipeline = Util.make_pipeline(file_path, steps)
    return run_pipeline()


# FIXME: need to refine filter_rows and make smart lists for filter_columns
# FIXME: fix load class to be able to update records or create new records
