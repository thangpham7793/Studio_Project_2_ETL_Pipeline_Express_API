import pandas as pd
import os
import sys
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from MSHA import (
    target_canvasses,
    target_columns,
    target_materials,
    target_statuses,
    target_types,
)


class Transform:

    # function to process the MSHA data
    def convert_msha(self,dataframe):

        df = dataframe


        #selects the columns that we need
        df = df[target_columns]
    

        is_target_status = df["CURRENT_MINE_STATUS"].apply(lambda x: x in target_statuses)
        is_target_type = df["CURRENT_MINE_TYPE"].apply(lambda x: x in target_types)
        # for every row, check if the primary_sic cell's value is in target_materials
        is_target_primary_material = df["PRIMARY_SIC"].apply(lambda x: x in target_materials)
        is_target_secondary_material = df["SECONDARY_SIC"].apply(
            lambda x: x in target_materials
        )
        is_target_material = is_target_primary_material | is_target_secondary_material

        is_target_primary_canvass = df["PRIMARY_CANVASS"].apply(
            lambda x: x in target_canvasses
        )
        is_target_secondary_canvass = df["SECONDARY_CANVASS"].apply(
            lambda x: x in target_canvasses
        )
        is_target_canvass = is_target_primary_canvass | is_target_secondary_canvass
        # now we combine all conditions into one big filter
        conditions = is_target_status & is_target_material & is_target_canvass & is_target_type

        final_data = df[conditions]

        return final_data

        


    def convert_texas_gps(self, dataframe):
    
        locator = Nominatim(user_agent = 'myGeocoder')

        

        df = dataframe
        
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

        #Arrays that define columns to keep and another arraay "Drop target" for dropping columns later in the code
        target_cols = ['site_name', 'additional_id', 'physical_type', 'physical_site_status','rn', 'county',"region", "phys_addr_line_1","phys_addr_city", 'phys_addr_state','phys_addr_zip', 'latitude', 'longitude']
        drop_target = ['location', 'point','additional_id', 'physical_type', 'physical_site_status','rn', 'county',"region", 'latitude', 'longitude']
        target_status = ['ACTIVE']
        address_status = ["Unknown"]


        #create a new dataframe df that only contains the target columns
        df = df[target_cols]

        #creates boolean values to use to filter rows for the column physical site status
        target_status_rows = df['physical_site_status'].apply(lambda x: x in target_status)
        df = df[target_status_rows]


        #drops rows containing "Unknown" 
        df[df.phys_addr_line_1 != 'UNKNOWN']
        df[df.phys_addr_line_1 != 'Unknown']

        #drops rows containins NA's in "phys_addr_line_1"
        df.dropna(subset = ["phys_addr_line_1"], inplace=True)


        #drops rows containins NA's in "phys_addr_zip"
        df.dropna(subset = ["phys_addr_zip"], inplace=True)

        #converts zip code to whole number then to a string
        #df["phys_addr_zip"] = df["phys_addr_zip"].astype(int)
        df["phys_addr_zip"] = df["phys_addr_zip"].astype(str)

        df['Address'] = df["phys_addr_line_1"] + ", " + df['phys_addr_state'] + ", " + df['phys_addr_zip'] + ", " + "UNITED STATES OF AMERICA"
        

        #create new column called address that combines the different address lines together

        
        df = df.drop(["latitude", "longitude"], axis = 1)

        # 1 - conveneint function to delay between geocoding calls
        #geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
        # 2- - create location column
        df['location'] = df['Address'].apply(geocode)
        # 3 - create longitude, laatitude and altitude from location column (returns tuple)
        df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
        # 4 - split point column into latitude, longitude and altitude columns
        df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)

        

        gps_df = df

        

        return gps_df



    def convert_texas(self,dataframe):
    
        df = dataframe

        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

        #Arrays that define columns to keep and another arraay "Drop target" for dropping columns later in the code
        target_cols = ['site_name', 'additional_id', 'physical_type', 'physical_site_status','rn', 'county',"region", "phys_addr_line_1","phys_addr_city", 'phys_addr_state','phys_addr_zip', 'latitude', 'longitude']
        drop_target = ['location', 'point','additional_id', 'physical_type', 'physical_site_status','rn', 'county',"region", 'latitude', 'longitude']
        target_status = ['ACTIVE']
        address_status = ["Unknown"]


        #create a new dataframe df2 that only contains the target columns
        df = df[target_cols]

        #creates boolean values to use to filter rows for the column physical site status
        target_status_rows = df['physical_site_status'].apply(lambda x: x in target_status)
        df = df[target_status_rows]

        df["phys_addr_zip"] = df["phys_addr_zip"].astype(str)

        df_mod = df

        return df_mod
            