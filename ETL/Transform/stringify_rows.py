import pandas as pd
import re

# path = "C:/Users/chick/Desktop/TRANSFORM_TEST.csv"
# df = pd.read_csv(path)


# function needs to occur after values have been turned into a string


def remove_non_char(value):
    """
    >>> remove_non_char('email@domain.com')
    'email@domain.com'
    >>> remove_non_char('word-with-hyphen')
    'word-with-hyphen'
    """
    # regex for finding non-characters
    non_char_regex = re.compile("[^A-Za-z0-9 \-#\.@]")
    # some are kept because
    # @ and . are for emails
    # # means number
    # - is for delimiter

    # replace most non-characters with empty string
    new_value = non_char_regex.sub("", value)
    return new_value


def stringify_rows(df):
    # this should probably go to the TRANSFORM class
    # turn all values into string (this should not be in this class though...)
    for col in df.columns:
        if col not in ["location", "latitude", "longitude"]:
            new_col = df[col].apply(lambda x: remove_non_char(str(x).lower().strip()))
            df[col] = new_col
    return df


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
