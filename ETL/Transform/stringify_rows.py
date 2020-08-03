import pandas as pd
import re

# path = "C:/Users/chick/Desktop/TRANSFORM_TEST.csv"
# df = pd.read_csv(path)


# function needs to occur after values have been turned into a string


def remove_non_char(value):
    # regex for finding non-char character
    non_char_regex = re.compile("[^A-Za-z0-9 ]")
    # replace all non-characters with empty string
    new_value = non_char_regex.sub("", value)
    return new_value


def stringify_rows(df):
    # this should probably go to the TRANSFORM class
    # turn all values into string (this should not be in this class though...)
    for col in df.columns:
        if col not in ["location"]:
            # maybe clean it up a bit more here (remove punctuations, etc.)
            df[col] = df[col].apply(lambda x: remove_non_char(str(x).lower().strip()))
    return df
