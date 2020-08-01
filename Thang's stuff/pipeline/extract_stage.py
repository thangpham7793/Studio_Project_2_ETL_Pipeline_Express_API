import pandas as pd

# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3

if __name__ == "__main__":
    # use absolute import if running file as main
    from Util import Util
    from extract_steps.get_extension import get_extension
    from extract_steps.are_columns_unique import are_columns_unique
    from extract_steps.no_unnamed_columns import no_unnamed_columns
else:
    # use relative import if the file is being imported by another one
    from . import Util
    from .extract_steps.get_extension import get_extension
    from .extract_steps.are_columns_unique import are_columns_unique
    from .extract_steps.no_unnamed_columns import no_unnamed_columns


switcher = {
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "csv": pd.read_csv,
    "txt": pd.read_csv,
}

# combine both conditions:
def is_valid_colnames(colnames):
    return no_unnamed_columns(colnames) and are_columns_unique(colnames)


def validate_colnames(df):
    # check if the existing colnames is valid first:
    if is_valid_colnames(df.columns):
        return df
    else:
        # if not, start checking the row from top to bottom (usally row 0 or 1 is the correct column names)
        for i in df.index:
            # print("Start checking row", i)
            r = df.iloc[i]
            # print(is_validif is_valid_colnames(r))
            if is_valid_colnames(r):
                # use this row as the column names
                df.columns = list(r)
                # drop the row before returning the df
                return df.drop(i)
        # still return the df in case no valid row is found,
        # but this is extremely unlikely
        return df


def read_file(file_path):
    ext = get_extension(file_path)
    try:
        if ext == "txt":
            df = switcher[ext](file_path, sep="|", encoding="unicode_escape")
        else:
            df = switcher[ext](file_path)
        return df
    except KeyError:
        print("Unknown Extension. Please pick a file of type txt, xlxs, csv, or xls")
        return "Failed"


def initial_clean_up(df):
    # removing duplicate columns
    # https://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns

    df = df.T.drop_duplicates().T
    # drop duplicate rows
    df = df.drop_duplicates()
    df = df.fillna("")
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )
    return df


extract_steps = [
    {"step": "READ_FILE", "function": read_file},
    {"step": "INITIAL_CLEAN_UP", "function": initial_clean_up},
    {"step": "VALIDATE_COLNAMES", "function": validate_colnames},
]

