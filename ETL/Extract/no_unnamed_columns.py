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


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
