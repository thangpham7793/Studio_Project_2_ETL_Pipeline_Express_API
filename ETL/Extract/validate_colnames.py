# check for duplicates
def are_columns_unique(colnames):
    """Check if all or most of the columns are unique
    
    @param colnames: list of string
    @return: boolean
    
    Tests

    >>> valid_list = ['A', 'B', 'C']
    >>> valid_list_2 = ['A', 'A', 'B', 'C']
    >>> invalid_list = ['A', 'A', 'A', 'A', 'A']
    >>> invalid_list_2 = ['A', 'A', 'A', 'A', 'A', 'B']
    >>> are_columns_unique(valid_list)
    True
    >>> are_columns_unique(valid_list_2)
    True
    >>> are_columns_unique(invalid_list)
    False
    >>> are_columns_unique(invalid_list_2)
    False
    >>> are_columns_unique(None)
    Error getting the length of column list
    >>> are_columns_unique([])
    Column list must not be empty
    """
    try:
        if len(colnames) == 0:
            print("Column list must not be empty")
            return
    except TypeError:
        print("Error getting the length of column list")
        return
    else:
        no_of_colnames = len(colnames)
        no_of_distinct_colnames = len(set(list(colnames)))
        # colnames must be unique! (plus 2 to allow for cases where one or two columns are duplicated)
        return no_of_colnames <= no_of_distinct_colnames + 2


def no_unnamed_columns(colnames):
    """Check whether a list of column name only has 0 or a few unnamed columns
    
    @param colnames: list of string
    @return: boolean
    
    Tests:
    
    >>> valid_list = ['Unnamed', 'A', 'B', 'C', 'D']
    >>> invalid_list = ['Unnamed', 'Unnamed', 'Unnamed']
    >>> none_list = None
    >>> empty_list = []
    >>> no_unnamed_columns(valid_list)
    True
    >>> no_unnamed_columns(invalid_list)
    False
    >>> no_unnamed_columns(None)
    Invalid type: Colnames must be a list
    >>> no_unnamed_columns(empty_list)
    False
    """

    no_of_unnamed = 0
    try:
        for col in colnames:
            if "Unnamed" in str(col):
                no_of_unnamed += 1
    except TypeError as err:
        print("Invalid type: Colnames must be a list")
    else:
        # if there are too many unnamed columns, probably all col names are unnamed!
        if no_of_unnamed >= len(colnames) / 2:
            return False
        else:
            return True


# combine both conditions:
def is_valid_colnames(colnames):
    return no_unnamed_columns(colnames) and are_columns_unique(colnames)


def validate_colnames(df):
    # check if the existing colnames is valid first:
    colnames = list(df.columns)
    if is_valid_colnames(colnames):
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


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
