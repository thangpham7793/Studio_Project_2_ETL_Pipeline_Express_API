import Util
import pandas as pd

from Extract.read_file import read_file
from Extract.basic_clean_up import basic_clean_up
from Extract.validate_colnames import validate_colnames

from Transform.fuzzy_col_filter import fuzzy_col_filter
from Transform.fuzzy_row_filter import fuzzy_row_filter
from Transform.add_location import add_location
from Transform.stringify_rows import stringify_rows

from Load.load_into_database import load_into_database

steps = [
    {"step": "READ_FILE", "function": read_file},
    {"step": "VALIDATE_COLNAMES", "function": validate_colnames},
    {"step": "BASIC_CLEAN_UP", "function": basic_clean_up},
    {"step": "FUZZY_COL_FILTER", "function": fuzzy_col_filter},
    {"step": "FUZZY_ROW_FILTER", "function": fuzzy_row_filter},
    # filter_columns must go first
    # to allow user or the program to pick out the latlng columns
    # filter rows reduce the number of modifications later
    {"step": "ADD_LOCATION", "function": add_location},
    {"step": "STRINGIFY_ROWS", "function": stringify_rows},
    {"step": "LOAD_INTO_DATABASE", "function": load_into_database},
]


def build_pipeline_and_run(file_path):
    # need to copy the steps since the recursive pipeline
    # will consume each step one by one
    pipeline_steps = steps.copy()
    run_pipeline = Util.make_pipeline(file_path, pipeline_steps)
    return run_pipeline()


main = Util.apply_on_all_files(build_pipeline_and_run)
