import pandas as pd

# path = "C:/Users/chick/Desktop/TRANSFORM_TEST.csv"
# df = pd.read_csv(path)
# df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

valid_status = ["active", "new mine", "intermittent"]


def filter_status(dataframe):

    df = dataframe

    for col in df.columns:
        if col == "physical_site_status":
            condition = df["physical_site_status"].apply(
                lambda status: status.lower().strip() in valid_status
            )
            df = df.loc[condition]
            return df

    return df


# filtered_df = filter_status(df)
# print(filtered_df.head())
