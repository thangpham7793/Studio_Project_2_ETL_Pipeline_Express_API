from pymongo import MongoClient
import pandas as pd
import dns


# URI string for connecting to the cloud MongoDB
MONGODB_URI = "mongodb+srv://thangpham7793:p7b6D7Y9KhUBCsU@usminesdatabase.jke71.mongodb.net/usminesdb?retryWrites=true&w=majority"
DB_NAME = "us-mines-locations"
DB_COLLECTION = "test"


def remove_empty_entry(doc):
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


def stringify_all_but_location(df):
    # this should probably go to the TRANSFORM class
    # turn all values into string (this should not be in this class though...)
    for col in df.columns:
        if col not in ["location"]:
            # maybe clean it up a bit more here (remove punctuations, etc.)
            df[col] = df[col].apply(lambda x: str(x).lower().strip())
    return df


def turn_df_into_json_docs(df):
    # flip the df before turning each column (which is essentially a row before the flip) into a dictionary (json)
    json_documents = df.T.to_dict()

    # remove all empty keys in each document in the dictionary
    for k in json_documents:
        remove_empty_entry(json_documents[k])

    return json_documents


# HERE'S PROBABLY WHERE THE LOAD CLASS ACTUALLY BEGINS
def initialize_collection():
    # connect to MongoDB
    client = MongoClient(MONGODB_URI)

    # open a database connection
    db = client[DB_NAME]

    # return a connection to the target collection
    return db[DB_COLLECTION]


def load_into_database(df):
    # transform df into a dictionary of json documents
    json_documents = turn_df_into_json_docs(df)

    # initialize the collection that receives these documents
    collection = initialize_collection()

    # TODO: which insert method should be used? (upsert, insert, etc.)
    # get the docs from the dictionary and turn them into a list
    # and then insert them into the collection
    collection.insert_many(list(json_documents.values()))
    return df
