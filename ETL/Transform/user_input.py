# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
from fuzzywuzzy import fuzz
import pandas as pd
from schema import mine_schema


file_path = "C:/Users/chick/Desktop/col_name_test.xlsx"
df = pd.read_excel(file_path)


col_suggestion = {}
all_names = {}

def populate_all_names(dataframe):
    
    counter = 1
    for key in mine_schema:
        all_names[counter] = key
        counter += 1


def pick_an_option(dictionary):
    
    print_dictionary(dictionary)
    col_choice = int(input("Choose a column name to rename too, keep it as it is or drop the column from the table"))
    return col_choice


def print_dictionary(dictionary):

    if len(dictionary) == 0:
        print("Dictionary is empty")
        return
    else:
        for key in dictionary:
            print("")
            print(str(key) + ". " + dictionary[key])


def col_suggestion(col):

    col = col
    col_suggestion = {0:"Show all choices"}
    counter = 1

    for key in mine_schema:
        score = (fuzz.token_set_ratio(col, key))
        if score > 70:
            col_suggestion[counter] = key
            counter += 1
    print(" ")
    print("Which column name would you like to rename " + col + " too?")

    #Checks if no matches are found
    if len(col_suggestion) == 1:
        choice = pick_an_option(all_names)
        print(" ")
        print("The user picks " + all_names[choice])
    else:
        choice = pick_an_option(col_suggestion)
        
        if choice == 0: #user not happy with choices
            choice = pick_an_option(all_names)
            print(" ")
            print("The user picks " + all_names[choice])









