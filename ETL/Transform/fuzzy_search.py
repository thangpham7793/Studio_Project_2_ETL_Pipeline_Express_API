#This code compares values in dictionary and column names and gives a score. 
# Then returns key as option and then asks if they want to change columns name to key name
#Need  to integrate into exsiting code so number of options for user is narrowed down
#based on score.

#could append key names that over 70 into list and print list items as menu options
# or could use 

from fuzzywuzzy import fuzz
import pandas as pd
from schema import mine_schema

file_path = "C:/Users/chick/Desktop/col_name_test.xlsx"
df = pd.read_excel(file_path)

def narrow_selection(dataframe):

  df = dataframe      

  for key, values in mine_schema.items():
    for value in values:
      for col in df.columns:
        score = (fuzz.token_set_ratio(col, value))
        if score > 70:
          print("1. " + key)    
          choice = input("What would you like to change " + col + " to?")
  


   

