from schema import mine_schema
from classes.Extract import Extract
from classes.Load import Load
import pandas as pd
from os import system, name


def update_schema():
    f = open("schema.py", "w")
    f.write(f"mine_schema = {mine_schema}")
    f.close()


# TODO: need to add a tag to determine which collections it belong to?
# TODO: should carry out some basic standardisation beforehand (lowercase etc.)
def check_if_colnames_in_saved_list(col):
    # this could be improved by having some fuzzy search
    for k in mine_schema:
        if k != "keep_it_as_it_is":
            # if colname is in the list of col names that have been changed, return the corresponding standardised col name.
            if col in mine_schema[k] or col is k:
                return {"result": True, "colname": k}
        else:
            # if the colname is in the list of unchanged columns, simply return it
            if col in mine_schema[k]:
                return {"result": True, "colname": col}
    # if the col name is not in the record, return false and ask for user's input
    return {"result": False}


def choose_dropped_columns(df):
    dropped_cols = []
    filter_dict = {}
    for col in df.columns:
        if col in mine_schema.keys():
            continue
        else:
            sample_values = list(df[col].unique())[0:5]
            print(f"Column '{col.upper()}' has some values like {sample_values}\n")
            # TODO: can carry out filtering right here (especially for columns with only a few values)
            # TODO: can remember invalid choices as well
            user_input = input(
                f"Would you like to keep column {col.upper()}? Type Y/N\n"
            )
            clear_screen()
            if user_input.lower() not in ["yes", "y", "ye"]:
                dropped_cols.append(col)
            else:
                check_result = check_if_colnames_in_saved_list(col)
                if check_result["result"] is True:
                    new_name = check_result["colname"]
                    if new_name != col:
                        print(f"Renaming {col} to {new_name}")
                    else:
                        print(f"Keeping {col} as it is.")
                else:
                    new_name = show_standardized_colnames(col)
                    if new_name != col:
                        print(f"Renaming {col} to {new_name}")
                    else:
                        print(f"Keeping {col} as it is.")
                df.rename(columns={col: new_name}, inplace=True)
    return df.drop(columns=dropped_cols)


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
        user_input = round(int(user_input), 0)
        if user_input == len(mine_schema) - 1:
            # TODO: could remember columns that are skipped (especially latitude and longitude since they get handled later)
            mine_schema["keep_it_as_it_is"].append(col)
            return col
        else:
            chosen_colname = list(mine_schema.keys())[user_input]
            mine_schema[chosen_colname].append(col)
            return chosen_colname


def main(df):
    df = choose_dropped_columns(df)
    update_schema()
    pd.DataFrame.to_csv(df, "./test.csv", index=False)
    return df


# https://www.geeksforgeeks.org/clear-screen-python/
def clear_screen():
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


if __name__ == "__main__":
    # TODO: need to turn this into a file-drop or select file_path (GUI?)
    file_path = "./data/TX/msw-facilities-texas.xls"
    extractor = Extract()
    loader = Load()
    df = extractor.to_df(file_path)
    df = main(df)
    # FIXME: results show that there are 'nan' fields being saved to the database and no location field is created. Could be because you load the data from a csv
    loader.load_into_database(df)

