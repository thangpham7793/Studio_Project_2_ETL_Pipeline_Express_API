import pymongo
from pymongo import MongoClient
from pymongo.errors import (
    BulkWriteError,
    OperationFailure,
    InvalidOperation,
    ConnectionFailure,
    ConfigurationError,
    ServerSelectionTimeoutError,
)
import pandas as pd
import dns
from typing import List, Union

# URI string for connecting to the cloud MongoDB
MONGODB_URI = "mongodb+srv://us-mines-database:us-mines-database@usminesdatabase.leaav.mongodb.net/us-mines-database?retryWrites=true&w=majority"
DB_NAME = "us-mines-database"
DB_COLLECTION = "locations"

# FIXME: there should be a separate collection for landfills


def remove_empty_entry(doc: dict) -> None:
    # store any key with empty value in an array to delete later
    # can't delete inside the loop because that would change the number of the keys
    if isinstance(doc, dict) == True:
        empty_key = []
        for k in doc:
            # check if the location field is a dict or not. If not, it needs to be deleted
            if k == "location" and type(doc["location"]) is dict:
                continue
            elif k in ["latitude", "longitude"]:
                continue
            # if there's a value missing, add the key to the list above
            elif doc[k].lower() in ["", "nan", "unknown", "no record"]:
                empty_key += [k]
        # if the list's empty, do nothing since there's no missing value
        if len(empty_key) == 0:
            pass
        else:
            # delete all keys in the dict with empty values based on the stored list
            for i in empty_key:
                del doc[i]
            # this function operates on each document, so we don't have to return anything
    else:
        print(f"Input must be of type dictionary!")
        return


def turn_df_into_json_docs(df: pd.DataFrame) -> Union[List[dict], pd.DataFrame]:
    if (isinstance(df, pd.DataFrame) and df.empty == False) == True:
        try:
            # flip the df before turning each column (which is essentially a row before the flip) into a dictionary (json)
            json_documents = df.T.to_dict()
        except AttributeError:
            print(f"Cannot ")
        # remove all empty keys in each document in the dictionary
        for k in json_documents:
            remove_empty_entry(json_documents[k])

        return list(json_documents.values())
    else:
        print(
            f"Invalid input. Either input is not a dataframe or the dataframe is empty"
        )
        return df


def initialize_collection(
    uri: str, db_name: str, db_collection: str
) -> pymongo.collection:
    # connect to MongoDB
    client = MongoClient(uri)

    # open a database connection
    db = client[db_name]

    # return a connection to the target collection
    return db[db_collection]


def define_primary_keys_for_query(doc: dict) -> dict:
    query = {}
    valid_pks = ["longitude", "latitude", "site_name", "controller", "operator"]

    # create composite pks to find a match in the database
    for k in valid_pks:
        if k in doc.keys():
            query[k] = doc[k]
    return query


def update_collection(
    collection: pymongo.collection, json_documents: List[dict]
) -> None:
    for doc in json_documents:
        try:
            query = define_primary_keys_for_query(doc)
        except TypeError as e:
            print(f"Failed to create query: {e}")

        # FIXME: an old record with a new coordinates will still create a duplicate record!
        # FIXME: probably need a separate module for reading data from Mongo
        # into Python to deal with duplicates.

        update = {"$set": doc}

        try:
            # set upsert = True to insert a new doc
            # if the query returns no matching doc

            # update every field that is present in the new record.
            # Existing fields that do not appear here
            # will still be kept in the database
            res = collection.update_one(query, update, upsert=True).raw_result
            # print(res)
        except (OperationFailure, NameError) as e:
            print(f"Could not insert document {new_data}: {e}\n")
            continue


def check_2dsphere_index(collection: pymongo.collection) -> None:
    """ Check if 2dsphere index exists and creates one if not
    
    ### Initialize database connection
    >>> col = initialize_collection(MONGODB_URI, DB_NAME, 'test_col')
    
    ### Add a sample record with a location field
    >>> col.insert_one({"location": [20, 20]}) # doctest: +ELLIPSIS
    <...>
    
    ### Should create a new index
    >>> check_2dsphere_index(col)
    Created 2dsphere index on field location
    
    ### Should inform index exists
    >>> check_2dsphere_index(col)
    2dsphere index already exists on field location
    
    ### Clean up
    >>> col.delete_many({}) # doctest: +ELLIPSIS
    <...>
    >>> col.drop_index('location_2dsphere')
    
    """
    try:
        indexes = collection.index_information()
    except (InvalidOperation, OperationFailure) as e:
        print(
            "Cannot access indexes! Please check them using Mongo Atlas, Shell or Compass!"
        )
        return
    # check if 2dsphere index exists
    if "location_2dsphere" in indexes.keys():
        print(f"2dsphere index already exists on field location")
        return
    else:
        try:
            collection.create_index([("location", "2dsphere")])
        except (OperationFailure, TypeError) as e:
            print(f"Error creating 2dsphere index: {e}")
            return
        print(f"Created 2dsphere index on field location")
        return


def load_into_database(df: pd.DataFrame) -> pd.DataFrame:

    # initialize empty placeholders
    json_documents = ""
    collection = ""

    try:
        # transform df into a dictionary of json documents
        json_documents = turn_df_into_json_docs(df)
    except AttributeError as e:
        print(f"Error making json documents: {e}")
        return df
    # initialize the collection that receives these documents
    try:
        collection = initialize_collection(MONGODB_URI, DB_NAME, DB_COLLECTION)
    except (ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError) as e:
        print(f"Error connecting to database: {e}")
        return df

    print(f"Finished making JSON documents.\n")
    print(json_documents[0])

    try:
        # NOTE: must use update_one to avoid inserting duplicates
        update_collection(collection, json_documents)
        # collection.insert_many(json_documents)
    except (KeyError, AttributeError, NameError) as e:
        print(f"There was an error inserting records into the database: {e}")

    # check to see if 2dsphere index exists
    check_2dsphere_index(collection)

    # return the final dataframe for checking
    return df


# https://stackoverflow.com/questions/21076460/how-to-convert-a-string-to-objectid-in-nodejs-mongodb-native-driver/21076589#21076589

# https://docs.mongodb.com/manual/reference/method/db.collection.update/

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
