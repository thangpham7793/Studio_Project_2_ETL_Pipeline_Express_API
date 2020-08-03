import pandas as pd


# path = "C:/Users/chick/Desktop/add_location_test.csv"
# df = pd.read_csv(path)
# df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')


def check_longitude(longitude):
    if type(longitude) == str:
        return longitude
    else:
        return -abs(longitude)


def check_latitude(latitude):
    if type(latitude) == str:
        return latitude
    else:
        return abs(latitude)


def add_location(df):
    # fill all NA values as string
    # df.fillna("", inplace=True)
    # this should probably go to the TRANSFORM class
    # if there's no long lat then pass and return df
    if ("longitude" not in list(df.columns)) or ("latitude" not in list(df.columns)):
        print("Skip Location!")
        return df

        # this should probably go to the TRANSFORM ROW class
    df["latitude"] = df["latitude"].apply(lambda x: check_latitude(x))
    df["longitude"] = df["longitude"].apply(lambda x: check_longitude(x))

    # make a new list to store the locations
    location_list = []
    # iterate through each row to make a nested location dictionary
    for i in df.index:
        row = df.loc[i]
        # if latlng is not a number, add an emptry string as the value
        if type(row["longitude"]) == str or type(row["latitude"]) == str:
            location_list.append("")
        else:
            # this is based on MongoDB's specification
            # { type: "Point", coordinates: [ 40, 5 ] }
            # https://docs.mongodb.com/manual/reference/geojson/#
            new_location = {
                "coordinates": [row["longitude"], row["latitude"]],
                "type": "Point",
            }
            location_list.append(new_location)
        # assign the new list as a new column
    df["location"] = location_list

    # drop the lat long cols
    df.drop(columns=["latitude", "longitude"], inplace=True)
    return df


# print(add_location(df))
