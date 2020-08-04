mine_schema = {
    "location": {"type": "Point", "coordinates": []},
    "mine_name": ["site_name"],
    "longitude": [],
    "latitude": [],
    "state": ["phys_addr_state"],
    "city": ["phys_addr_city"],
    "street_address": ["phys_addr_line_1"],
    "zip": ["phys_addr_zip"],
    "fips_county_code": ["fips_cnty_cd"],
    "fips_county": ["county", "fips_cnty_nm"],
    "physical_status": ["physical_site_status", "current_mine_status"],
    "legal_status": [],
    "primary_sic": [],
    "primary_sic_code": [],
    "secondary_sic": [],
    "secondary_sic_code": [],
    "primary_canvass": [],
    "primary_canvass_code": [],
    "secondary_canvass_code": [],
    "secondary_canvass": [],
    "controller": [],
    "operator": [],
    "directions_to_mine": ["near_phys_loc_txt"],
    "nearest_town": ["near_phys_loc_city"],
    "mail_address": [],
    "email": [],
    "phone": [],
    "office_address": [],
    "website_URL": [],
    "keep_it_as_it_is": [],
    "dropped_cols": [],
}

