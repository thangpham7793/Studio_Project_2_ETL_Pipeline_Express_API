from extract_stage import extract_steps
from Util import Util

first_input = "./data/texas_mines_data.xlsx"

run_extract_stage = Util.make_pipeline_stage(first_input, "EXTRACT", extract_steps)
run_extract_stage()
