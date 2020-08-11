if __name__ == "__main__":
    from schema import mine_schema
else:
    from .schema import mine_schema

import pandas as pd
from os import system, name, path
from fuzzywuzzy import fuzz
from typing import Dict, List, Union

Schema = Dict[str, List[str]]
Options = Dict[int, str]

# HELPERS
# https://www.geeksforgeeks.org/clear-screen-python/
def clear_screen():
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def update_schema(mine_schema: Schema):
    # for google colab
    folder_path = "/content/drive/My Drive/ETL/Transform/schema.py"
    try:
        f = open(folder_path, "w")
    except FileNotFoundError:
        # on local machine
        try:
            folder_path = path.abspath("Transform")
            f = open(f"{folder_path}/schema.py", "w")
        except FileNotFoundError:
            print("Could not update schema!")
            return
    print(folder_path)
    f.write(f"mine_schema = {mine_schema}")
    f.close()


# check if colname has been processed before
def check_if_colnames_in_saved_list(colname: str, mine_schema: Schema) -> dict:
    # if the colname is in the list of unchanged columns, simply return it
    if colname in mine_schema["keep_it_as_it_is"]:
        return {"result": True, "colname": colname}
    # if the colname is in the list of dropped columns, return None to drop it
    if colname in mine_schema["dropped_cols"]:
        return {"result": True, "colname": "dropped"}
    # if colname is in the list of colname names that have been changed
    # or it has the same name as the standardised name (key),
    # return the corresponding standardised colname name.
    for k in mine_schema:
        if colname in mine_schema[k] or colname == k:
            return {"result": True, "colname": k}

    # if the column name is not in the dict, return False to ask for user input
    return {"result": False}


# make a dict with options indexed from 1 based on all the standard colnames

# remove standard colnames that have been chosen by the user to avoid duplicate colnames
def trim_options(option_dict: Options, picked_names: List[str]) -> Options:
    if len(picked_names) == 0:
        return option_dict
    to_remove_indexes = []
    for n in picked_names:
        for key, val in option_dict.items():
            if n == val:
                to_remove_indexes.append(key)
                break
    for i in to_remove_indexes:
        del option_dict[i]
        return option_dict


def make_full_option_dict(mine_schema: Schema, picked_names: List[str]) -> Options:

    option_dict = {}
    counter = 1
    for key in mine_schema:
        option_dict[counter] = key
        counter += 1
    return trim_options(option_dict, picked_names)


def make_fuzzy_match_option_dict(
    colname: str, mine_schema: Schema, picked_names: List[str]
) -> Options:

    fuzzy_match_option_dict = {}
    counter = 1

    methods = [
        fuzz.ratio,
        fuzz.partial_ratio,
        fuzz.token_sort_ratio,
        fuzz.partial_token_sort_ratio,
        fuzz.token_set_ratio,
        fuzz.partial_token_set_ratio,
    ]
    # try all methods from the strictest
    for key in mine_schema:
        for m in methods:
            score = m(colname, key)
            if score > 70:
                fuzzy_match_option_dict[counter] = key
                counter += 1
                break

    fuzzy_match_option_dict[len(fuzzy_match_option_dict) + 1] = "show_all_choices"
    fuzzy_match_option_dict[len(fuzzy_match_option_dict) + 1] = "dropped_cols"
    return fuzzy_match_option_dict


def make_option_dict(
    colname: str, mine_schema: Schema, picked_names: List[str], fuzzy: bool = True
) -> Options:
    if fuzzy:
        option_dict = make_fuzzy_match_option_dict(colname, mine_schema, picked_names)
    else:
        option_dict = make_full_option_dict(mine_schema, picked_names)
    return option_dict


# pretty print dictionary of options
def print_options(option_dict: Options) -> None:
    if len(option_dict) == 0:
        print("Option dictionary must not be empty!")
        return
    else:
        for key in option_dict:
            val = option_dict[key]
            # add horizontal tab to odd index to print 3 columns of options
            if key % 3 != 0:
                if len(val) >= 15:
                    print(f"{key}. {val}", end="\t" * 3)
                else:
                    print(f"{key}. {val}", end="\t" * 4)
            else:
                print(f"{key}. {val}", end="\n")


# Get user choice
def get_user_choice(colname: str, option_dict: Options) -> str:
    print(f"\nAvailable Options for {colname.upper()}:\n")
    print_options(option_dict)
    col_choice: str
    invalid_input = True
    while invalid_input:
        col_choice = input(f"\n")
        # validate user input
        if col_choice.isnumeric() and int(col_choice) in option_dict.keys():
            invalid_input = False
            print(f"Choose fuzzy match {col_choice}")
            break
        else:
            clear_screen()
            print("Please type in a number from the list.\n")
            print(f"\nAvailable Options:\n")
            print_options(option_dict)
    clear_screen()
    print("\n" * 2)
    return option_dict[int(col_choice)]


def get_new_name(
    df: pd.DataFrame, colname: str, mine_schema: Schema, picked_names: List[str]
) -> str:
    clear_screen()
    sample_values = list(df[colname].unique())[0:5]
    print(
        f"\nColumn '{colname.upper()}' has some values like {sample_values}\nType in a number to choose a column name to rename {colname.upper()} to, keep it as it is or drop the column from the table\n"
    )
    # make a fuzzy option dict
    option_dict = make_option_dict(colname, mine_schema, picked_names, fuzzy=True,)
    # if there's no fuzzy match, present all choices
    if len(option_dict) == 2:
        print("No fuzzy matches found, showing all choices")
        option_dict = make_option_dict(colname, mine_schema, picked_names, fuzzy=False)
        return get_user_choice(colname, option_dict)
    # if user's not happy with the fuzzy match
    user_choice = get_user_choice(colname, option_dict)
    if user_choice == "show_all_choices":
        clear_screen()
        option_dict = make_option_dict(colname, mine_schema, picked_names, fuzzy=False)
        return get_user_choice(colname, option_dict)
    # if user picks one of the fuzzy matches
    else:
        return user_choice


def add_source_column(dataframe: pd.DataFrame) -> pd.DataFrame:
    df = dataframe.copy()
    is_msha = input("Is this the MSHA dataset? Y/N\n\n")
    while is_msha.lower() not in ["yes", "y", "ye", "n", "no"]:
        print("Invalid answer. Please type in your answer again.\n\n")
        is_msha = input("Is this data set MSHA? Y/N")
    if is_msha.lower() in ["yes", "y", "ye"]:
        df["source"] = "msha"
    else:
        df["source"] = "other"
    return df


def add_site_type_column(dataframe: pd.DataFrame) -> pd.DataFrame:
    df = dataframe.copy()
    print(df.head(10))
    which_type = input("\nWhat is this dataset about? 1. Mines\t2. Landfill\t 3. Others\n\n")
    invalid_input = True
    while invalid_input:
        if which_type in ["1", "2", "3"]:
            invalid_input = False
        else:
            print("Invalid answer. Please type in 1 , 2  or 3.\n\n")
            which_type = input("\nWhat is this dataset about? 1. Mines\t2. Landfill\t 3. Others\n\n")
    if which_type == "1":
        df["site_type"] = "mine"
    elif which_type == "2":
        df["site_type"] = "landfill"
    else:
        df["site_type"] = "others"
    return df

def add_dataset_name_col(dataframe: pd.DataFrame) -> pd.DataFrame:
    df = dataframe.copy()
    print(df.head(10))
    dataset_name = input("\nPlease type in the name of this dataset.\n\n")
    not_confirmed = True
    while not_confirmed:
        confirm = input("\nAre you sure you want to name the dataset as " + dataset_name.upper() + "? Y/N\n\n")
        if confirm.lower() in ["y","ye","yes"]:
            not_confirmed = False

        elif confirm.lower() in ["n","no"]:
            dataset_name = input("\nPlease type in the name of this dataset.\n\n")
            
        else:
            print("Invalid answer please type in y or n")
            
    df["dataset_name"] = dataset_name
 
    return df


# update schema as the last step
def update_schema(mine_schema: Schema) -> None:
    # for google colab
    folder_path = "/content/drive/My Drive/ETL/Transform/schema.py"
    try:
        f = open(folder_path, "w")
    except FileNotFoundError:
        # on local machine
        try:
            folder_path = path.abspath("Transform")
            f = open(f"{folder_path}/schema.py", "w")
        except FileNotFoundError:
            print("Could not update schema!")
            return
    print(folder_path)
    f.write(f"mine_schema = {mine_schema}")
    f.close()


# MAIN FUNCTION
def fuzzy_col_filter(dataframe: pd.DataFrame) -> pd.DataFrame:
    dropped_cols = []
    # store standard colnames that have been picked to avoid duplicates
    picked_names = []
    df = dataframe.copy()
    for col in df.columns:
        check_result = check_if_colnames_in_saved_list(col, mine_schema)
        # check if the colname has been processed before
        if check_result["result"] == True:
            # if yes, check if the colname has been kept or dropped
            if check_result["colname"] != "dropped":
                # if it's kept, save it to a variable
                new_name = check_result["colname"]
                # check if the colname should be renamed or not
                if new_name != col:
                    # if different, this means that it needs to be renamed
                    print(f"Renaming {col.upper()} to {new_name.upper()}\n")
                    df.rename(columns={col: new_name}, inplace=True)
                # if it's not, simply keep it and move on
                else:
                    print(f"Keeping {col.upper()} as it is.\n")
            # if it's dropped before, add it to the current drop list
            else:
                dropped_cols.append(col)
        # if it's a new colname, show users some sample values, and then ask for input
        else:
            new_name = get_new_name(df, col, mine_schema, picked_names=picked_names)
            # add col to drop list if user says no
            if new_name == "dropped_cols":
                print(f"Dropping {col.upper()}.\n")
                dropped_cols.append(col)
            else:
                # if the choice is different, rename it
                if new_name != col and new_name != "keep_it_as_it_is":
                    print(f"Renaming {col.upper()} to {new_name.upper()}\n")
                    df.rename(columns={col: new_name}, inplace=True)
                    picked_names.append(new_name)
                else:
                    # add the colname to the keep it as it is list
                    print(f"Keeping {col.upper()} as it is.\n")
            # also update the schema accordingly
            mine_schema[new_name].append(col)

    # ask users if this is msha data-set
    df = add_source_column(df)

    # ask users if it's about mines or other types (like landfills)
    df = add_site_type_column(df)
    clear_screen()
    # gets the name of the dataset
    # TODO: Come up with a standardised naming system 
    df = add_dataset_name_col(df) 

    # write the updated schema to file
    update_schema(mine_schema)
    return df.drop(columns=dropped_cols)
