# TODO: write tests for each stage


def no_duplicate_columns(df):
    return len(df.columns) == len(set(df.columns))


# TODO: LOAD:
# Should insert all new records
# Should not overwrite added fields on subsequent updates
# Should show updated information
