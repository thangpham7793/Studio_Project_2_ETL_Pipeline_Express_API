import pandas as pd

# path = "C:/Users/chick/Desktop/TRANSFORM_TEST.csv"
# df = pd.read_csv(path)
# df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

valid_physical_status = [
    "active",
    "new mine",
    "intermittent",
    "active mining",
]

valid_legal_status = [
    "effective",
    "admin continued",
    "6 - permit coverage granted",
    "current",
    "approved",
    "administrative continuance",
    "permitted",
    "admin",
    "released",
    "issued",
    "current",
    "newly permitted",
    "reissuance",
    "issued",
    "acknowledged",
]

valid_mine_types = ["Surface", "Facility"]


def filter_rows_by_col(df, colname, valid_values):

    if colname in df.columns:
        condition = df[colname].apply(
            lambda val: str(val).lower().strip() in valid_values
        )
        return df.loc[condition]
    return df


def filter_rows(df):
    filtered_df_1 = filter_rows_by_col(df, "physical_status", valid_physical_status)
    filtered_df_2 = filter_rows_by_col(
        filtered_df_1, "legal_status", valid_legal_status
    )
    filtered_df_3 = filter_rows_by_col(filtered_df_2, "mine_type", valid_mine_types)
    return filtered_df_3


# filtered_df = filter_status(df)
# print(filtered_df.head())
