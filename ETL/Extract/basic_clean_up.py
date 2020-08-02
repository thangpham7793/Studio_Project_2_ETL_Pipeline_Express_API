import re
import pandas as pd


def remove_non_char_from_colnames(colnames):
    """Remove non-characters from each column names
    
    Should return colnames with only characters and numbers. 
    
    The list should also be of the same length
    
    >>> input = ['a1,;:', '"b"$%#12', 'c?\;])de', '']
    >>> new_list = remove_non_char_from_colnames(input)
    >>> new_list
    ['a1', 'b12', 'cde', '']
    >>> len(new_list) == len(input)
    True
    """
    non_char_regex = re.compile("[^A-Za-z0-9 ]")
    new_columns = list(map(lambda colname: non_char_regex.sub("", colname), colnames))
    new_columns = list(
        map(lambda colname: re.compile(" ").sub("_", colname), new_columns)
    )
    return new_columns


def basic_clean_up(df):

    # make colnames lowercase, remove whitespace
    df.columns = list(map(lambda colname: colname.strip().lower(), df.columns))

    # fill all na values with empty string
    df = df.fillna("")
    # https://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns
    # removing duplicate columns
    df = df.T.drop_duplicates().T
    # drop duplicate rows
    df = df.drop_duplicates()

    # remove white space
    df.columns = remove_non_char_from_colnames(df.columns)
    return df


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
