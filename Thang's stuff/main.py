from pipeline.extract_stage import extract_steps
from pipeline.Util import Util

file_path = "../ETL_pipeline/data/TX/msw-facilities-texas.xls"
run_extract_stage = Util.make_pipeline_stage(file_path, "EXTRACT", extract_steps)
res = run_extract_stage()
