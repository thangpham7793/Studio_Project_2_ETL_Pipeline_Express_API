if __name__ == "__main__":
    # use absolute import if running file as main
    from are_columns_unique import are_columns_unique
    from no_unnamed_columns import no_unnamed_columns
else:
    # use relative import if the file is being imported by another one
    from .are_columns_unique import are_columns_unique
    from .no_unnamed_columns import no_unnamed_columns


# combine both conditions:
def is_valid_colnames(colnames):
    return no_unnamed_columns(colnames) and are_columns_unique(colnames)


def validate_colnames(df):
    # check if the existing colnames is valid first:
    colnames = list(df.columns)
    if is_valid_colnames(colnames):
        return df
    else:
        # if not, start checking the row from top to bottom (usally row 0 or 1 is the correct column names)
        for i in df.index:
            # print("Start checking row", i)
            r = df.iloc[i]
            # print(is_validif is_valid_colnames(r))
            if is_valid_colnames(r):
                # use this row as the column names
                df.columns = list(r)
                # drop the row before returning the df
                return df.drop(i)
        # still return the df in case no valid row is found,
        # but this is extremely unlikely
        return df
