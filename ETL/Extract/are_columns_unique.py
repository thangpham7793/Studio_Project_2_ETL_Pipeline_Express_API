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


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
