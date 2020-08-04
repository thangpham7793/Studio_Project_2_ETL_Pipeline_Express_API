import pandas as pd


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
    # if there's no long lat then pass and return df
    if ("longitude" not in list(df.columns)) or ("latitude" not in list(df.columns)):
        print("Skip Location!")
        return df

        # this should probably go to the TRANSFORM ROW class
    df.loc[:, "latitude"] = df["latitude"].apply(lambda x: check_latitude(x))
    df.loc[:, "longitude"] = df["longitude"].apply(lambda x: check_longitude(x))

    # make a new list to store the locations
    location_list = []
    # iterate through each row to make a nested location dictionary
    for i in df.index:
        row = df.loc[i]
        # if latlng is 0 or a string, append an empty string as the location field
        # FIXME: need to account for other ways of representing latlong, like S/W, or in minutes...
        if type(row["longitude"]) == str or type(row["latitude"]) == str:
            location_list.append("")
        elif int(row["longitude"]) == 0 or int(row["latitude"]) == 0:
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
