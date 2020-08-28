## US-MINES-API DOCUMENTATION

All requests should begin with

- https://us-mines-api.herokuapp.com

or if you're testing it locally:

- http://localhost:3000/ (or the port number that is set in your .env)

### REQUESTs FOR MINES

#### GET

1. all available materials:

- /mines/materials

2. all mines regardless of materials (default radius is 200 miles):

- /mines/@{longitude},{latitude}

3. Get mines by material and gps coordinates within a particular radius:

- /mines/{material}/@{longitude},{latitude},{radius}

4. Get One Mine by Id

- /mines/{id}

Examples:

- http://us-mines-api.herokuapp.com/mines/@-87.5,30.23

- https://us-mines-api.herokuapp.com/mines/sand+and+gravel/@-87,30,80
- http://us-mines-api.herokuapp.com/mines/sand+and+gravel/@-87.5,30.23,120
- http://us-mines-api.herokuapp.com/mines/sand/@-145.5,60.23,50
- http://us-mines-api.herokuapp.com/mines/limestone/@-70.5,45.23

- http://us-mines-api.herokuapp.com/mines/5f326ec5903f3e0d204c26da

### REQUESTs FOR LANDFILLS

#### GET

Similar to Mines but much simpler since there's no material filter.

1. Get all landfills by latlng (default radius is 200 miles):

- /landfills/@{longitude},{latitude}

3. Get mines by material and gps coordinates within a particular radius

- /landfills/@{longitude},{latitude},{radius}

3. Get One Landfill by Id

- /landfills/{id}

Examples:

- http://us-mines-api.herokuapp.com/landfills/@-100,35
- http://us-mines-api.herokuapp.com/landfills/@-102,36.23,50
- http://us-mines-api.herokuapp.com/landfills/5f326ddb903f3e0d204bd8ff

### NOTES:

1. Validation:

Material cannot contain non-characters and should be separated by "+".

The longitude, latitude, and radius are separated by a comma.

Longitude must be negative and latitude and radius must be larger than 0.

Longitude and latitude should also be in their acceptable range (-180 to 180, -90 to 90, respectively)

2. Tips:

GPS Coorditates for cities in United States are:

- Latitude: from 19.50139 to 64.85694
- Longitude: from -161.75583 to -68.01197 .

All Search Results include an unique ID of each record and are sorted based on distance from nearest to furthest.

Geospatial Queries will return results sorted based on distance, from nearest to furthest. Radius is optional and the default is 200 miles.
