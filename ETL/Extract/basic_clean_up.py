import re
import pandas as pd


def remove_non_char(values):
    """Remove non-characters from each column names and substitude whitespace with underscore
    
    Should return value with only characters and numbers. 
    
    The list should also be of the same length
    
    >>> input = ['a1,;:', '"b" $%#12', 'c ?\;])de', '']
    >>> new_list = remove_non_char(input)
    >>> new_list
    ['a1', 'b_12', 'c_de', '']
    >>> len(new_list) == len(input)
    True
    """
    non_char_regex = re.compile("[^A-Za-z0-9 ]")
    # replace all non-characters with empty string
    new_values = list(map(lambda value: non_char_regex.sub("", value), values))
    # replace white space with underscore
    new_values = list(map(lambda value: re.compile(" ").sub("_", value), new_values))
    return new_values


def basic_clean_up(df):
    # make colnames lowercase, remove whitespace
    df.columns = list(map(lambda colname: str(colname).strip().lower(), df.columns))

    # fill all na values with empty string
    df = df.fillna("")
    # https://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns
    # removing duplicate columns
    df = df.T.drop_duplicates().T
    # drop duplicate rows
    df = df.drop_duplicates()

    # remove white space
    df.columns = remove_non_char(df.columns)
    return df


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
