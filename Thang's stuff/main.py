from schema import mine_schema
from pipeline.Extract import Extract
from pipeline.Load import Load
from pipeline.Transform_Columns import Transform_Columns
from pipeline.Filter import Filter
from pipeline.Util import Util

import pandas as pd

# Eric would have to manually enter this
FILE_PATH = "../ETL_pipeline/data/filtered_mine_data.csv"

# initialize each class in the pipeline
extractor = Extract()
columns_transformer = Transform_Columns()
filterer = Filter()
# rows_transformer = Transform_Rows()
loader = Load()


def main(df):
    df = extractor.to_df(FILE_PATH)
    df = columns_transformer.choose_dropped_columns(df)
    Util.update_schema()
    pd.DataFrame.to_csv(df, "./test.csv", index=False)
    return df


if __name__ == "__main__":
    main()

