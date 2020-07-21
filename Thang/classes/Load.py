import pandas as pd
import sys
import os
from string import Template

# load itself doesn't know the file_path
class Load:

    switcher = {
        "xls": pd.read_excel,
        "xlsx": pd.read_excel,
        "csv": pd.read_csv,
        "txt": pd.read_csv,
    }

    summary_template = Template(
        """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="../../log_style.css" />
  <title>Document</title>
</head>
<body>
  ${summary}
</body>
</html>                                
"""
    )

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
            # print("Original column is invalid!")
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

    def load_success_summary(self, df, file_path):
        # NOTE: this assumes that the file is located inside ./data/dir/state/...
        state_folder = file_path.split("/")[-2]
        # in case of nested folder within a state folder (like TX/Permits/...)
        if len(state_folder) > 2:
            state_folder = file_path.split("/")[-3]

        print(file_path)

        file_name = file_path.split("/")[-1]

        for char in [" ", "#", "?", ":", ";", "%"]:
            file_name = file_name.replace(char, "_")

        log_path = f"./logs/{state_folder}/{file_name.strip()}_load_log.html"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        log = open(log_path, "w")

        try:
            # print out the first 5 values of each column
            sample_record = ""
            for col in df.columns:
                values = df[col].unique()

                # print all values if there are less than 50 unique values, or just print the first 50 unique values
                if len(values) < 50:
                    sample_values = values
                else:
                    sample_values = values[0:50]
                sample_record += f"<li style='font-weight: normal;'> <strong>{col}</strong>: {sample_values}</li>"

            summary = f"""
                      <header>
                      <h1>
                        <a name="{state_folder}">{state_folder}</a>
                      </h1>
                        <a href="../../index.html">Back to Index</a>
                        <h2>{file_path}</h2>

                        <h4>Number of Rows and Columns</h4> 
                        <p>{df.shape}</p>
                        <h4>Columns</h4> 
                      </header>
                      <main>
                        <div>
                        
                          {list(df.columns)}
                        
                        </div>
                        
                        <div>
                          <h4>Sample Record</h4>
                          <ul>
                          {sample_record}
                          </ul>
                        </div>
                        <footer>
                            <small><a href="#{state_folder}">Back to Top</a></small>
                            <small><a href="../../overview.html">Back to Index</a></small>
                        </footer>
                      </main>
                      """
        except:
            print(f"There was an error summarizing {file_path}")
            summary = (
                f"<p>There was an error summarizing {file_path}: \n{sys.exc_info()}</p>"
            )

        finally:
            log.write(self.summary_template.substitute(summary=summary))
            log.close()

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
                self.load_success_summary(df, file_path)
            except:
                print(
                    f"There was an error writing success summary for {file_path}: \n{sys.exc_info()}"
                )
        return df

