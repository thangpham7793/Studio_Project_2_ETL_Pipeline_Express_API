from fuzzywuzzy import fuzz
import pandas as pd

# valid physical statuses
valid_physical_statuses = [
    "active",
    "new mine",
    "intermittent",
    "active mining",
]


# valid legal status
valid_legal_statuses = [
    "effective",
    "admin continued",
    "6 - permit coverage granted",
    "current",
    "approved",
    "administrative continuance",
    "permitted",
    "admin",
    "released",
    "issued",
    "current",
    "newly permitted",
    "reissuance",
    "issued",
    "acknowledged",
]

# FIXME: valid mine type (not using this since there are too many valid options). It's better to use filter
# based on a list of invalid values.
valid_mine_types = ["surface", "facility"]
invalid_mine_types = ["underground"]


# valid_sic
valid_sic = [
    "cement",
    "clay ceramic refractory mnls.",
    "common clays nec",
    "common shale",
    "construction sand and gravel",
    "crushed broken basalt",
    "crushed broken granite",
    "crushed broken limestone nec",
    "crushed broken marble",
    "crushed broken mica",
    "crushed broken quartzite",
    "crushed broken sandstone",
    "crushed broken slate",
    "crushed broken stone nec",
    "crushed broken traprock",
    "dimension basalt",
    "dimension granite",
    "dimension limestone",
    "dimension marble",
    "dimension mica",
    "dimension quartzite",
    "dimension sandstone",
    "dimension slate",
    "dimension stone nec",
    "dimension traprock",
    "lime",
    "nonmetal",
    "sand common",
    "sand industrial nec",
]

# for testing purposes
invalid_sic = [
    "tungsten ore",
    "turquoise",
    "uranium ore",
    "uranium-vanadium ore",
    "vanadium ore",
    "vermiculite",
    "wollastonite",
    "zeolites",
    "zinc",
    "zirconium ore",
]


def is_in_target_list(val, values):
    """Decide if a value is valid based on partial matching
    
    ### Should return true when the matches are exact    

    1. Valid SIC
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_sic), valid_sic))
    >>> len(results) == len(valid_sic)
    True
    
    2. Valid legal status
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_legal_statuses), valid_legal_statuses))
    >>> len(results) == len(valid_legal_statuses)
    True
    
    3. Valid physical status
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_physical_statuses), valid_physical_statuses))
    >>> len(results) == len(valid_physical_statuses)
    True
    
    4. Valid mine types
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_mine_types), valid_mine_types))
    >>> len(results) == len(valid_mine_types)
    True
    
    ### Should return true for partial matches
    
    1. Partial SIC matches
    >>> partial_matches = ['traprock', 'sand', 'clay ceramic']
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_sic), partial_matches))
    >>> print(results)
    ['traprock', 'sand', 'clay ceramic']
    
    2. Partial legal status matches
    >>> partial_matches = ['permitted', 'continuance', 'continued', 'granted']
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_legal_statuses), partial_matches))
    >>> print(results)
    ['permitted', 'continuance', 'continued', 'granted']
    
    3. Partial physical status matches
    >>> partial_matches = ['new', 'mining', 'active']
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_physical_statuses), partial_matches))
    >>> print(results)
    ['new', 'mining', 'active']
    
    ### Should return true for matches with no spaces
    
    1. SIC
    >>> partial_matches = ['dimensiontraprock', 'sandandgravel', 'clayceramic']
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_sic), partial_matches))
    >>> print(results)
    ['dimensiontraprock', 'sandandgravel', 'clayceramic']
    
    2. Legal status
    >>> partial_matches = ['administrativecontinuance', 'newlypermitted', 'admincontinued', 'permitcoveragegranted']
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_legal_statuses), partial_matches))
    >>> print(results)
    ['administrativecontinuance', 'newlypermitted', 'admincontinued', 'permitcoveragegranted']
    
    3. Physical status
    >>> partial_matches = ['newmine', 'activemining']
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_physical_statuses), partial_matches))
    >>> print(results)
    ['newmine', 'activemining']
    
    ### Should exclude false invalid values
    (not as important since we can afford redundant storage rather than missing out on potentially useful leads)
        
    1. Invalid SIC
    >>> results = list(filter(lambda val: is_in_target_list(val, valid_sic), invalid_sic))
    >>> print(results)
    []

    """
    methods = [
        fuzz.ratio,
        fuzz.partial_ratio,
        fuzz.token_sort_ratio,
        fuzz.partial_token_sort_ratio,
        fuzz.token_set_ratio,
        fuzz.partial_token_set_ratio,
    ]
    # try all methods from the strictest
    for m in methods:
        val = str(val).lower().strip()
        if m(val, values) > 50:
            return True
    return False


def filter_rows_by_invalid_vals(df, colname, invalid_values):
    try:
        if colname in df.columns:
            condition = df[colname].apply(
                lambda val: not is_in_target_list(val, invalid_values)
            )
            return df.loc[condition]
        else:
            return df
    except AttributeError as e:
        print(f"There was an error filtering rows: {e}")


def filter_rows_by_valid_vals(df, colname, valid_values):
    try:
        if colname in df.columns:
            condition = df[colname].apply(
                lambda val: is_in_target_list(val, valid_values)
            )
            return df.loc[condition]
        else:
            return df
    except AttributeError as e:
        print(f"There was an error filtering rows: {e}")


# for cases where a valid column could be in mutliple columns.
# Like a sic could be in either primary_sic or secondary_sic
def filter_rows_by_many_cols(df, colnames, valid_values):
    conditions = []
    try:
        for col in colnames:
            if col in df.columns:
                condition = df[col].apply(
                    lambda val: is_in_target_list(val, valid_values)
                )
                conditions.append(condition)
    except AttributeError as e:
        print(f"There was an error filtering rows: {e}")

    if len(conditions) == 1:
        return df[conditions[0]]
    elif len(conditions) == 2:
        return df[conditions[0] | conditions[1]]
    else:
        return df


def reset_index(df):
    try:
        return df.reset_index().drop(columns=["index"])
    except AttributeError as e:
        print(f"Cannot reset dataframe index: {e}")
        return df


def fuzzy_row_filters(df):
    print(len(df))
    filtered_df_1 = filter_rows_by_valid_vals(
        df, "physical_status", valid_physical_statuses
    )
    print(f"Down to {len(filtered_df_1)}")
    filtered_df_2 = filter_rows_by_valid_vals(
        filtered_df_1, "legal_status", valid_legal_statuses
    )
    print(f"Down to {len(filtered_df_2)}")
    filtered_df_3 = filter_rows_by_invalid_vals(
        filtered_df_2, "mine_type", invalid_mine_types
    )
    print(f"Down to {len(filtered_df_3)}")
    # filtered_df_4 = filter_rows_by_valid_vals(filtered_df_3, "primary_sic", valid_sic)
    # filtered_df_5 = filter_rows_by_valid_vals(filtered_df_4, "secondary_sic", valid_sic)
    # print(f"Down to {len(filtered_df_5)}")
    filtered_df_4 = filter_rows_by_many_cols(
        filtered_df_3, ["primary_sic", "secondary_sic"], valid_sic
    )
    print(f"Down to {len(filtered_df_4)}")
    return reset_index(filtered_df_4)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
