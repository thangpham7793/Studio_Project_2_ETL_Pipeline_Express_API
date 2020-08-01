from pymongo import MongoClient
import pandas as pd
import dns
import os
from dotenv import load_dotenv

load_dotenv()

# URI string for connecting to the cloud MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "us-mines-locations"
DB_COLLECTION = "msha_v2"


class Load:
    # this should probably go to the TRANSFORM ROW class
    def check_longitude(self, longitude):
        if type(longitude) == str:
            return longitude
        else:
            return -abs(longitude)

    def check_latitude(self, latitude):
        if type(latitude) == str:
            return latitude
        else:
            return abs(latitude)

    # this should probably go to the TRANSFORM ROW class
    def add_location(self, df):
        # fill all NA values as string
        df.fillna("", inplace=True)
        # this should probably go to the TRANSFORM class
        # if there's no long lat then pass and return df
        if ("longitude" not in list(df.columns)) or (
            "latitude" not in list(df.columns)
        ):
            print("Skip Location!")
            return df

        # this should probably go to the TRANSFORM ROW class
        df["latitude"] = df["latitude"].apply(lambda x: self.check_latitude(x))
        df["longitude"] = df["longitude"].apply(lambda x: self.check_longitude(x))

        # make a new list to store the locations
        location_list = []
        # iterate through each row to make a nested location dictionary
        for i in df.index:
            row = df.loc[i]
            # if there's an emptry string, skip to the next row
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

    def remove_empty_entry(self, doc):
        # store any key with empty value in an array to delete later
        # can't delete inside the loop because that would change the number of the keys
        empty_key = []
        for k in doc:
            # check if the location field is a dict or not. If not, it needs to be deleted
            if k == "location" and type(doc["location"]) is dict:
                continue
            # if there's a value missing, add the key to the list above
            elif doc[k].lower() in ["", "nan", "unknown"]:
                empty_key += [k]
        # if the list's empty, do nothing since there's no missing value
        if len(empty_key) == 0:
            pass
        else:
            # delete all keys in the dict with empty values based on the stored list
            for i in empty_key:
                del doc[i]
            # this function operates on each document, so we don't have to return anything

    def stringify_all_but_location(self, df):
        # this should probably go to the TRANSFORM class
        # turn all values into string (this should not be in this class though...)
        for col in df.columns:
            if col not in ["location"]:
                # maybe clean it up a bit more here (remove punctuations, etc.)
                df[col] = df[col].apply(lambda x: str(x).lower().strip())
        return df

    def add_location_and_turn_into_json_docs(self, df):
        # this should probably go to the TRANSFORM class
        # basically piping df through the functions above
        # FIXME: find places where PANDAS may throw a view vs df error
        df = self.add_location(df)
        df = self.stringify_all_but_location(df)

        # flip the df before turning each column (which is essentially a row before the flip) into a dictionary (json)
        json_documents = df.T.to_dict()

        # remove all empty keys in each document in the dictionary
        for k in json_documents:
            self.remove_empty_entry(json_documents[k])
        # HERE THE RETURNED VALUE IS A DICTIONARY OF JSON DOCS, NOT A DF. THIS IS PROBABLY THE LAST FUNCTION IN TRANSFORM CHAIN
        return json_documents

    # HERE'S PROBABLY WHERE THE LOAD CLASS ACTUALLY BEGINS
    def initialize_collection(self):
        # connect to MongoDB
        client = MongoClient(MONGODB_URI)
        # open a database connection ("test" = the name of the database)
        db = client[DB_NAME]

        # return a connection to the target collection ("msha" = the name of the collection)
        return db[DB_COLLECTION]

    # THIS PROBABLY NEEDS TO BE REWRITTEN SINCE THE add_location_and_turn_into_json_docs
    # SHOULD BE IN THE TRANSFORM CLASS
    # IN THAT CASE THIS FUNCTION PROBABLY ACCEPTS A DICTIONARY OF JSON DOCS INSTEAD OF A DATAFRAME
    def load_into_database(self, df):
        # transform df into a dictionary of json documents
        json_documents = self.add_location_and_turn_into_json_docs(df)

        # initialize the collection that receives these documents
        collection = self.initialize_collection()

        # TODO: which insert method should be used? (upsert, insert, etc.)
        # get the docs from the dictionary and turn them into a list
        # and then insert them into the collection (table)
        collection.insert_many(list(json_documents.values()))
        return json_documents
