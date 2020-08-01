from schema import mine_schema
from Util import Util
import pandas as pd


class Transform_Columns:

    # TODO: need to add a tag to determine which collections it belong to?
    # TODO: should carry out some basic standardisation beforehand (lowercase etc.)
    def check_if_colnames_in_saved_list(self, col):
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
            f"'{col.upper()}' has not been processed before. Please help me Dear Good User!\n"
        )
        return {"result": False}

    def choose_dropped_columns(self, df):
        dropped_cols = []
        filter_dict = {}
        for col in df.columns:
            check_result = check_if_colnames_in_saved_list(col)
            if check_result["result"] == True:
                if check_result["colname"] != None:
                    new_name = check_result["colname"]
                    if new_name != col:
                        print(f"Renaming {col} to {new_name}")
                    else:
                        print(f"Keeping {col} as it is.")
                else:
                    dropped_cols.append(col)
            else:
                sample_values = list(df[col].unique())[0:5]
                print(f"Column '{col.upper()}' has some values like {sample_values}\n")
                # TODO: can carry out filtering right here (especially for columns with only a few values)
                # TODO: can remember invalid choices as well
                user_input = input(
                    f"Would you like to keep column {col.upper()}? Type Y/N\n"
                )
                Util.clear_screen()
                if user_input.lower() not in ["yes", "y", "ye"]:
                    dropped_cols.append(col)
                else:
                    new_name = show_standardized_colnames(col)
                    if new_name != col and new_name != "keep_it_as_it_is":
                        print(f"Renaming {col} to {new_name}")
                    else:
                        print(f"Keeping {col} as it is.")
                    df.rename(columns={col: new_name}, inplace=True)
        # updating the list of dropped columns
        for col in dropped_cols:
            if col not in mine_schema["dropped_cols"]:
                mine_schema["dropped_cols"].append(col)
        return df.drop(columns=dropped_cols)

    def show_standardized_colnames(self, col):

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
        Util.clear_screen()
        if not user_input.isnumeric():
            user_input = input(f"Please type in a number\n")
        elif int(user_input) < 0 or int(user_input) > len(mine_schema) - 1:
            user_input = input(
                f"Please type in a number within 0 and {len(mine_schema)-1}"
            )
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

