import pandas as pd
import re
from typing import List, Union

# TODO: should the latlng be rounded to a certain length?
# FIXME: would break if comma is the delimiter
# check if latlng is in degree-min-sec form
def is_degree_min_sec(val: str) -> Union[bool, None]:
    """
    >>> is_degree_min_sec('"-23.5')
    False
    >>> is_degree_min_sec('-87')
    False
    >>> is_degree_min_sec(' -87.4564')
    False
    >>> is_degree_min_sec("33*23'11''")
    True
    >>> is_degree_min_sec("15.23* 23.4** 45.5''")
    True
    """
    try:
        return len(parse_degree_min_sec(val)) >= 2
    except TypeError as e:
        return


def parse_degree_min_sec(val: str) -> Union[List[float], str]:
    """parse latlng in degree-min-sec form
    >>> parse_degree_min_sec("33*23'11''")
    [33.0, 23.0, 11.0]
    >>> parse_degree_min_sec("15-23-45")
    [15.0, 23.0, 45.0]
    >>> parse_degree_min_sec("15.23* 23.4** 45.5''")
    [15.23, 23.4, 45.5]
    >>> parse_degree_min_sec("15.23* 23.4** 45.5''")
    [15.23, 23.4, 45.5]
    """
    non_digit = re.compile("[^\d.]")
    try:
        val_list = non_digit.sub(" ", val).split(" ")
    except TypeError:
        return val
    numbers_only = []
    # filter and turn all digit strings to float
    try:
        for v in val_list:
            if v != "":
                numbers_only += [float(v)]
        return numbers_only
    except ValueError:
        return val


# https://stackoverflow.com/questions/21298772/how-to-convert-latitude-longitude-to-decimal-in-python
def convert(val_list: List[float]) -> float:
    return sum(float(x) / 60 ** n for n, x in enumerate(val_list))


def remove_non_digit(val: Union[str, float]) -> Union[str, float]:
    """remove non-char from value
    >>> remove_non_digit('-123a')
    '123'
    >>> remove_non_digit("'-123.454")
    '123.454'
    >>> remove_non_digit("0.00")
    '0.00'
    >>> remove_non_digit('')
    ''
    >>> remove_non_digit(-123)
    -123
    """
    # match all char except for digits, dots, and commas
    non_digit = re.compile("[^\d.,]")
    # replace matched chars with empty space,
    # so that float() doesn't throw an error later
    try:
        return non_digit.sub("", val)
    except TypeError:
        return val


def check_longitude(longitude: Union[str, float]) -> float:
    """parse longitude from a possible string and make sure longitude is negative
    >>> check_longitude('111.25')
    -111.25
    >>> check_longitude('111.25W')
    -111.25
    >>> check_longitude('no record')
    0
    >>> check_longitude('0.00')
    0
    >>> check_longitude("111.25")
    -111.25
    >>> check_longitude('111.25')
    -111.25
    >>> check_longitude(-111.25)
    -111.25
    
    """
    if type(longitude) == str:
        longitude = longitude.strip()
        if is_degree_min_sec(longitude):
            degree_min_sec = parse_degree_min_sec(longitude)
            if isinstance(degree_min_sec, list):
                return -convert(degree_min_sec)
            else:
                return longitude
        else:
            longitude = remove_non_digit(longitude)
            # if there's no number and it's an empty string
            if len(longitude) == 0:
                return 0
            # if it's just 0
            elif float(longitude) == 0:
                return 0
            # there's a value
            else:
                return -abs(float(longitude))
    else:
        try:
            return -abs(longitude)
        except TypeError:
            return longitude


def check_latitude(latitude: Union[str, float]) -> float:
    """parse latitude from a possible string and make sure latitude is positive
    >>> check_latitude('35.54')
    35.54
    >>> check_latitude('35.54E')
    35.54
    >>> check_latitude('no record')
    0
    >>> check_latitude('0.00')
    0
    >>> check_latitude("35.54")
    35.54
    >>> check_latitude(35.54)
    35.54
    >>> check_latitude(-35.54)
    35.54
    """
    if type(latitude) == str:
        latitude = latitude.strip()
        if is_degree_min_sec(latitude):
            degree_min_sec = parse_degree_min_sec(latitude)
            if isinstance(degree_min_sec, list):
                return convert(degree_min_sec)
            else:
                return latitude

        else:
            latitude = remove_non_digit(latitude)
            # if it's an empty string
            if len(latitude) == 0:
                return 0
            # if it's just 0
            elif float(latitude) == 0:
                return 0
            # there's a value
            else:
                return abs(float(latitude))
    else:
        try:
            return abs(latitude)
        except TypeError:
            return latitude


def add_location(df: pd.DataFrame) -> pd.DataFrame:
    # if there's no long lat then pass and return df
    if ("longitude" not in list(df.columns)) or ("latitude" not in list(df.columns)):
        print("Skip Location!")
        return df

    # parse latlng (if needed) and make sure lng is negative and lat is positive
    df.loc[:, "latitude"] = df["latitude"].apply(lambda x: check_latitude(x))
    df.loc[:, "longitude"] = df["longitude"].apply(lambda x: check_longitude(x))

    # make a new list to store the locations
    location_list = []
    # iterate through each row to make a nested location dictionary
    for i in df.index:
        row = df.loc[i]
        # append an empty string as the location field
        # if latlng is 0, a string, or out of range, location is an emptry string
        if type(row["longitude"]) == str or type(row["latitude"]) == str:
            location_list.append("")
        elif row["longitude"] == 0 or row["latitude"] == 0:
            location_list.append("")
        elif (
            row["longitude"] < -180
            or row["longitude"] > 180
            or row["latitude"] > 90
            or row["latitude"] < -90
        ):
            location_list.append("")
        else:
            # this is based on MongoDB's specification to create geo indexes
            # { type: "Point", coordinates: [ 40, 5 ] }
            # https://docs.mongodb.com/manual/reference/geojson/#
            new_location = {
                "coordinates": [row["longitude"], row["latitude"]],
                "type": "Point",
            }
            location_list.append(new_location)
        # assign the new list as a new column
    df["location"] = location_list
    # keep lat long as part of the composite key
    return df


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
