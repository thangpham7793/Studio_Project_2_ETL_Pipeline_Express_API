from pymongo import MongoClient
from pymongo.errors import BulkWriteError, OperationFailure
import pandas as pd
import dns


# URI string for connecting to the cloud MongoDB
MONGODB_URI = "mongodb+srv://thangpham7793:p7b6D7Y9KhUBCsU@usminesdatabase.jke71.mongodb.net/usminesdb?retryWrites=true&w=majority"
DB_NAME = "us-mines-locations"
DB_COLLECTION = "test"

# FIXME: there should be a separate collection for landfills


def remove_empty_entry(doc):
    # store any key with empty value in an array to delete later
    # can't delete inside the loop because that would change the number of the keys
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


def turn_df_into_json_docs(df):
    # flip the df before turning each column (which is essentially a row before the flip) into a dictionary (json)
    json_documents = df.T.to_dict()

    # remove all empty keys in each document in the dictionary
    for k in json_documents:
        remove_empty_entry(json_documents[k])

    return list(json_documents.values())


# HERE'S PROBABLY WHERE THE LOAD CLASS ACTUALLY BEGINS
def initialize_collection():
    # connect to MongoDB
    client = MongoClient(MONGODB_URI)

    # open a database connection
    db = client[DB_NAME]

    # return a connection to the target collection
    return db[DB_COLLECTION]


def update_collection(collection, json_documents):
    for doc in json_documents:
        # use a composite primary key as filter (can enforce this in the schema as well)
        # but don't set it in the database. Looking up doc by site_name is needed
        # because there are many sites with missing longitude and latitude
        query = {
            "site_name": doc["site_name"],
            "longitude": doc["longitude"],
            "latitude": doc["latitude"],
        }

        # update every field that is present in the new record. Existing fields that
        # do not appear here will still be kept in the database

        # # must remove location, longitude and latitude before inserting because they are unique indexes
        # new_data = doc.copy()
        # del new_data["longitude"]
        # del new_data["latitude"]
        # del new_data["location"]
        update = {"$set": doc}

        try:
            # set upsert = True to insert a new doc
            # if the query returns no matching doc
            collection.update_one(query, update, upsert=True)
        except (OperationFailure, NameError) as e:
            print(f"Could not insert document {new_data}: {e}\n")
            continue


def load_into_database(df):
    # transform df into a dictionary of json documents
    json_documents = turn_df_into_json_docs(df)

    # initialize the collection that receives these documents
    collection = initialize_collection()

    print(json_documents[0])

    invalid_input = True
    is_new_data = ""
    while invalid_input:
        is_new_data = input(
            "\nIs this the first time this data set is stored in the database? Y/N\n\n"
        )
        if is_new_data.lower() in ["y", "ye", "yes", "n", "no"]:
            invalid_input = False
        else:
            print("Please enter yes or no!")
    # if new, use insert_many
    if is_new_data in ["y", "ye", "yes"]:
        try:
            collection.insert_many(json_documents)
        except (BulkWriteError, OperationFailure) as e:
            print(f"Could not insert documents: {e}\n")
    else:
        try:
            update_collection(collection, json_documents)
        except (KeyError, AttributeError, NameError) as e:
            print(f"There was an error inserting records into the database: {e}")
    # return the final dataframe for checking
    return df


# https://stackoverflow.com/questions/21076460/how-to-convert-a-string-to-objectid-in-nodejs-mongodb-native-driver/21076589#21076589

# https://docs.mongodb.com/manual/reference/method/db.collection.update/ upsert?

# this would allow new records to be added, but what about old ones? Update retains the id though.

# what you want is to use the primary key within each document. Maybe ID and Name? What are the chances of duplicates?

# alright so you should use db.collection.update({query}, {$set: {new record}})
# but query should contain a unique compound index for each record (mine_name ? company name? + location?) This would only update fields and keep new fields that have been added

# FIXME: what happens if there are multiple duplicates 2dspere indexes

