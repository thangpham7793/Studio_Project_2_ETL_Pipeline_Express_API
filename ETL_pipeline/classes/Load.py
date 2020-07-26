import pandas as pd
import sys
from classes.Summary import Summary

summarizer = Summary()


class Load:

    # like a switch statement in Java, to look up the matching pd.read_file function
    # for a file extension
    switcher = {
        "xls": pd.read_excel,
        "xlsx": pd.read_excel,
        "csv": pd.read_csv,
        "txt": pd.read_csv,
    }

    def get_extension(self, file_path):
        try:
            ext = file_path.split(".")[-1]
            return ext
        except:
            print("File Path Must Have an Extension Followed by A Dot")

    def no_unnamed(self, colnames):
        no_of_unnamed = 0
        for col in colnames:
            if "Unnamed" in str(col):
                no_of_unnamed += 1
        # if there are too many unnamed columns, probably all col names are unnamed!
        if no_of_unnamed >= len(colnames) / 2:
            return False
        else:
            return True

    # check for duplicates
    def is_unique_index_col(self, colnames):
        no_of_colnames = len(colnames)
        no_of_distinct_colnames = len(set(list(colnames)))
        # colnames must be unique! (plus 2 to allow for cases where one or two columns are duplicated)
        return no_of_colnames <= no_of_distinct_colnames + 2

    # combine both conditions:
    def is_valid_colnames_list(self, colnames):
        return self.no_unnamed(colnames) and self.is_unique_index_col(colnames)

    def check_colnames(self, df):
        # check if the existing colnames is valid first:
        if self.is_valid_colnames_list(df.columns):
            return df
        else:
            # if not, start checking the row from top to bottom (usally row 0 or 1 is the correct column names)
            for i in df.index:
                # print("Start checking row", i)
                r = df.iloc[i]
                # print(is_valid_colnames_list(r))
                if self.is_valid_colnames_list(r):
                    # use this row as the column names
                    df.columns = list(r)
                    # drop the row before returning the df
                    return df.drop(i)
            # still return the df in case no valid row is found,
            # but this is extremely unlikely
            return df

    def to_df(self, file_path, make_html_summary=False):
        ext = self.get_extension(file_path)
        try:
            if ext == "txt":
                df = self.switcher[ext](file_path, sep="|", encoding="unicode_escape")
            else:
                df = self.switcher[ext](file_path)
        except:
            print(
                f"There was an error parsing {file_path} using Pandas: \n{sys.exc_info()}"
            )
        # removing duplicate columns
        # https://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns
        df = df.T.drop_duplicates().T

        # drop duplicate rows
        df = df.drop_duplicates()
        df = df.fillna("no record")

        try:
            # check for unnamed columns
            df = self.check_colnames(df)

        except:
            print(
                f"There was an error checking the column names of {file_path}: \n{sys.exc_info()}"
            )

        if make_html_summary == True:
            try:
                summarizer.load_success_summary(df, file_path)
            except:
                print(
                    f"There was an error writing success summary for {file_path}: \n{sys.exc_info()}"
                )
        return df

