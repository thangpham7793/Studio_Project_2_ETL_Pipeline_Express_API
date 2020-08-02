import pandas as pd

# path = "C:/Users/chick/Desktop/TRANSFORM_TEST.csv"
# df = pd.read_csv(path)


#function needs to occur after values have been turned into a string

def rows_to_lower(dataframe):

    df = dataframe

    for col in df:
        df[col] = df[col].str.strip().str.lower().str.replace('(', '').str.replace(')', '')

    return df




