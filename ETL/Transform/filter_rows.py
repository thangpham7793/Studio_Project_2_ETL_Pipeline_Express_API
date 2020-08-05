import pandas as pd

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

valid_mine_types = ["surface", "facility"]


def filter_rows_by_col(df, colname, valid_values):
    try:
        if colname in df.columns:
            condition = df[colname].apply(
                lambda val: str(val).lower().strip() in valid_values
            )
            return df.loc[condition]
        else:
            return df
    except AttributeError as e:
        print(f"There was an error filtering rows: {e}")


def reset_index(df):
    return df.reset_index().drop(columns=["index"])


def filter_rows(df):
    filtered_df_1 = filter_rows_by_col(df, "physical_status", valid_physical_status)
    filtered_df_2 = filter_rows_by_col(
        filtered_df_1, "legal_status", valid_legal_status
    )
    filtered_df_3 = filter_rows_by_col(filtered_df_2, "mine_type", valid_mine_types)
    return reset_index(filtered_df_3)
