import re
import pandas as pd
from typing import List


def remove_non_char(colnames: List[str]) -> List[str]:
    """Remove non-characters from each column names and substitude whitespace with underscore
    
    Should return colnames with only characters and numbers. 
    
    >>> input = ['a1,;:', '"b" $%12', 'c ?\;])de', 'mine_name', 'permit #']
    >>> new_list = remove_non_char(input)
    >>> new_list
    ['a1', 'b_12', 'c_de', 'mine_name', 'permit_#']
    
    The new colname list should also be of the same length
    
    >>> len(new_list) == len(input)
    True
    """
    non_char_regex = re.compile("[^A-Za-z0-9 _#]")
    # replace most non-characters in col names with empty string
    # # means number
    # _ is for delimiter
    new_colnames = list(map(lambda colname: non_char_regex.sub("", colname), colnames))
    # replace white space with underscore
    new_colnames = list(
        map(lambda colname: re.compile(" ").sub("_", colname), new_colnames)
    )
    return new_colnames


def basic_clean_up(df: pd.DataFrame):
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
