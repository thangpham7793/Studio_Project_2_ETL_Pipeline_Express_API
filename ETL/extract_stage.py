from Extract.read_file import read_file
from Extract.basic_clean_up import basic_clean_up
from Extract.validate_colnames import validate_colnames


extract_steps = [
    {"step": "READ_FILE", "function": read_file},
    {"step": "VALIDATE_COLNAMES", "function": validate_colnames},
    {"step": "INITIAL_CLEAN_UP", "function": basic_clean_up},
]

