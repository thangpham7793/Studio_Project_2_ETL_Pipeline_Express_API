import pandas as pd

# interesting stuff: https://github.com/catalyst-cooperative/pudl/
# https://datahub.io/zaneselvans/pudl-msha#data-cli (mostly for references)
# some fields are based on this form https://www.msha.gov/support-resources/forms-online-filing/2018/05/23/legal-identification-report


# read data into pandas dataframe (table)

df = pd.read_csv("./data/Mines.txt", sep="|", header=None, encoding="unicode_escape")
df.columns = list(df.loc[0, :])
df.drop([0], inplace=True)
pd.DataFrame.to_csv(df, "./data/raw_mines_data.csv", index=False)
df = pd.read_csv("./data/raw_mines_data.csv")

# read definition into a table for lookup
definitions = pd.read_csv("./data/field_definitions.txt", sep="|")
definitions.set_index("Field Name", inplace=True)
# write definitions to a csv file
pd.DataFrame.to_csv(
    definitions, "./data/field_definitions.csv"
)  # write definitions to a csv file
pd.DataFrame.to_csv(definitions, "./data/field_definitions.csv")


# a small function to quickly get the definition of a field/col
def getDef(colname):
    return definitions.loc[colname.upper()]["Description"]


# no. of rows and cols
df.shape


from MSHA import (
    target_canvasses,
    target_columns,
    target_materials,
    target_statuses,
    target_types,
)


data = df[target_columns]


# form a true/false vector from one of the column
is_target_status = data["CURRENT_MINE_STATUS"].apply(lambda x: x in target_statuses)


# the result is down to just over 12000 when applied the status filter
len(df[is_target_status])


is_target_type = data["CURRENT_MINE_TYPE"].apply(lambda x: x in target_types)


len(df[is_target_type])


# create two true/false vectors based on each product column

# for every row, check if the primary_sic cell's value is in target_materials
is_target_primary_material = df["PRIMARY_SIC"].apply(lambda x: x in target_materials)
is_target_secondary_material = df["SECONDARY_SIC"].apply(
    lambda x: x in target_materials
)

# any mine whose primary OR secondary product fall into the list count.
is_target_material = is_target_primary_material | is_target_secondary_material


# testing above condition. Seems like only half of the mines produce what Eric wants
len(data[is_target_material])


# same as above, but for canvass this time
is_target_primary_canvass = data["PRIMARY_CANVASS"].apply(
    lambda x: x in target_canvasses
)
is_target_secondary_canvass = data["SECONDARY_CANVASS"].apply(
    lambda x: x in target_canvasses
)

# combine into one condition
is_target_canvass = is_target_primary_canvass | is_target_secondary_canvass


# now we combine all conditions into one big filter
conditions = is_target_status & is_target_material & is_target_canvass & is_target_type


filtered_data = data[conditions]
len(filtered_data)

# save filtered_data to a csv file
pd.DataFrame.to_csv(filtered_data, "./data/filtered_mine_data.csv", index=False)

