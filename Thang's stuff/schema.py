mine_schema = {
    "location": {"type": "Point", "coordinates": []},
    "current_mine_name": ["site_name"],
    "state": ["phys_addr_state"],
    "city": ["phys_addr_city"],
    "street_address": ["phys_addr_line_1"],
    "zip": ["phys_addr_zip"],
    "fips_county_cd": [],
    "fips_county_nm": ["county", "fips_cnty_nm"],
    "physical_site_status": ["physical_site_status", "current_mine_status"],
    "primary_sic": [],
    "primary_sic_cd": [],
    "secondary_sic": [],
    "secondary_sic_cd": [],
    "primary_canvass": [],
    "primary_canvass_cd": [],
    "secondary_canvass_cd": [],
    "secondary_canvass": [],
    "controller_name": ["current_controller_name"],
    "operator_name": ["current_operator_name"],
    "directions_to_mine": ["near_phys_loc_txt"],
    "nearest_town": ["near_phys_loc_city"],
    "mail_address": [],
    "email": [],
    "phone": [],
    "office_address": [],
    "website_URL": [],
    "keep_it_as_it_is": [
        "physical_type",
        "legal_status",
        "region",
        "phys_addr_line_2",
        "phys_addr_zip+4",
        "near_phys_loc_zip",
        "latitude",
        "longitude",
        "current_mine_type",
        "bom_state_cd",
        "fips_cnty_cd",
        "primary_sic_cd_1",
        "secondary_sic_cd_1",
    ],
    "dropped_cols": [],
}

