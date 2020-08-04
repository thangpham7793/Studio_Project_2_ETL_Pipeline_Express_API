mine_schema = {'location': {'type': 'Point', 'coordinates': []}, 'site_name': ['mine_name', 'site__facility'], 'mine_type': [], 'longitude': ['long', 'lng', 'gps longitude', 'gps long', 'gps lng'], 'latitude': ['lat', 'gps latitude', 'gps lat'], 'state': ['phys_addr_state'], 'city': ['phys_addr_city'], 'street_address': ['phys_addr_line_1'], 'zip': ['phys_addr_zip'], 'fips_county_code': ['fips_cnty_cd'], 'fips_county': ['county', 'fips_cnty_nm'], 'physical_status': ['physical_site_status', 'current_mine_status'], 'legal_status': [], 'primary_sic': [], 'primary_sic_code': ['primary_sicnaics_code'], 'secondary_sic': [], 'secondary_sic_code': [], 'primary_canvass': [], 'primary_canvass_code': [], 'secondary_canvass_code': [], 'secondary_canvass': [], 'controller': [], 'operator': ['owner__operator'], 'directions_to_mine': ['near_phys_loc_txt'], 'nearest_town': ['near_phys_loc_city'], 'mail_address': [], 'email': [], 'phone': [], 'office_address': [], 'website_URL': [], 'keep_it_as_it_is': ['program', 'physical_type', 'legal_status_date', 'region', 'phys_addr_line_2', 'phys_addr_zip4', 'near_phys_loc_zip', 'permit', 'date_issued'], 'dropped_cols': ['additional_id', 'rn', 'near_phys_loc_state']}