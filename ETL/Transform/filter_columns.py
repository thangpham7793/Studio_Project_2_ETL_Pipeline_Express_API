if __name__ == "__main__":
    from schema import mine_schema
else:
    from .schema import mine_schema

import pandas as pd
from os import system, name, path


# https://www.geeksforgeeks.org/clear-screen-python/
def clear_screen():
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def update_schema():
    folder_path = path.abspath("Transform")
    print(folder_path)
    f = open(f"{folder_path}/schema.py", "w")
    f.write(f"mine_schema = {mine_schema}")
    f.close()


def check_if_colnames_in_saved_list(col):
    # this could be improved by having some fuzzy search
    # if the colname is in the list of unchanged columns, simply return it
    if col in mine_schema["keep_it_as_it_is"]:
        return {"result": True, "colname": col}
    # if the colname is in the list of dropped columns, return None to drop it
    if col in mine_schema["dropped_cols"]:
        return {"result": True, "colname": None}
    # if colname is in the list of col names that have been changed
    # or it has the same name as the standardised name (key),
    # return the corresponding standardised col name.
    for k in mine_schema:
        if col in mine_schema[k] or col == k:
            return {"result": True, "colname": k}
    # if the column name is not in the dict, return False to ask for user input
    print(
        f"'{col.upper()}' has not been processed before. Let me know if you want to keep it!\n"
    )
    return {"result": False}


def show_standardized_colnames(col):

    for index, k in enumerate(mine_schema.keys()):
        if index % 2 == 0:
            if len(k) <= 8:
                print(f"{index}. {k}", end="\t" * 4)
            else:
                print(f"{index}. {k}", end="\t" * 3)
        else:
            print(f"{index}. {k}", end="\n")
    print(
        "\n\nAbove are the list of important column names that need to be standardized."
    )
    user_input = input(
        f'Please choose one that matches "{col.upper()}" or keep it as it is by TYPING IN a number.\n'
    )
    clear_screen()
    if not user_input.isnumeric():
        user_input = input(f"Please type in a number\n")
    elif int(user_input) < 0 or int(user_input) > len(mine_schema) - 1:
        user_input = input(f"Please type in a number within 0 and {len(mine_schema)-1}")
    else:
        # FIXME: need to remove chosen choices to avoid having duplicate columns
        # which causes error later!
        user_input = round(int(user_input), 0)
        if user_input == len(mine_schema) - 1:
            mine_schema["keep_it_as_it_is"].append(col)
            return col
        else:
            chosen_colname = list(mine_schema.keys())[user_input]
            mine_schema[chosen_colname].append(col)
            return chosen_colname


def add_source_column(dataframe):
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


def filter_columns(dataframe):
    dropped_cols = []
    df = dataframe.copy()
    for col in df.columns:
        check_result = check_if_colnames_in_saved_list(col)
        if check_result["result"] == True:
            if check_result["colname"] != None:
                new_name = check_result["colname"]
                if new_name != col:
                    print(f"Renaming {col} to {new_name}")
                    df.rename(columns={col: new_name}, inplace=True)
                else:
                    print(f"Keeping {col} as it is.")
            else:
                dropped_cols.append(col)
        else:
            sample_values = list(df[col].unique())[0:5]
            print(f"Column '{col.upper()}' has some values like {sample_values}\n")

            user_input = input(
                f"Would you like to keep column {col.upper()}? Type Y/N\n\n"
            )
            clear_screen()
            while user_input.lower() not in ["yes", "y", "ye", "n", "no"]:
                print("Invalid answer. Please type in your answer again.\n\n")
                is_msha = input(
                    f"Would you like to keep column {col.upper()}? Type Y/N\n"
                )
            if user_input.lower() not in ["yes", "y", "ye"]:
                dropped_cols.append(col)
            else:
                new_name = show_standardized_colnames(col)
                print("Changing name!")
                if new_name != col and new_name != "keep_it_as_it_is":
                    print(f"Renaming {col} to {new_name}")
                    df.rename(columns={col: new_name}, inplace=True)
                else:
                    print(f"Keeping {col} as it is.")
    # updating the list of dropped columns
    for col in dropped_cols:
        if col not in mine_schema["dropped_cols"]:
            mine_schema["dropped_cols"].append(col)
    df = add_source_column(df)
    clear_screen()
    update_schema()
    return df.drop(columns=dropped_cols)
