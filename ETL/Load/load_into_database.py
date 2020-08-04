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


def update_collection(json_documents):
    for doc in json_documents:
        # use a composite primary key as filter (can enforce this in the schema as well)
        query = {
            "site_name": doc["site_name"],
            "longitude": doc["longitude"],
            "latitude": doc["latitude"],
        }

        update = {"$set": doc}

        try:
            collection.update_one(query, update, upsert=True)
        except:
            print(f"Could not insert document {doc}\n")
            continue


def load_into_database(df):
    # transform df into a dictionary of json documents
    json_documents = turn_df_into_json_docs(df)

    # initialize the collection that receives these documents
    collection = initialize_collection()

    print(json_documents[0])
    # collection.insert_many(list(json_documents.values())) this should only be used if this is a completely new data set... update_one is slow but is safe.
    try:
        update_collection(json_documents)
    except (KeyError, AttributeError) as e:
        print(f"There was an error inserting records into the database: {e}")

    return df


# https://stackoverflow.com/questions/21076460/how-to-convert-a-string-to-objectid-in-nodejs-mongodb-native-driver/21076589#21076589

# https://docs.mongodb.com/manual/reference/method/db.collection.update/ upsert?

# this would allow new records to be added, but what about old ones? Update retains the id though.

# what you want is to use the primary key within each document. Maybe ID and Name? What are the chances of duplicates?

# alright so you should use db.collection.update({query}, {$set: {new record}})
# but query should contain a unique compound index for each record (mine_name ? company name? + location?) This would only update fields and keep new fields that have been added
