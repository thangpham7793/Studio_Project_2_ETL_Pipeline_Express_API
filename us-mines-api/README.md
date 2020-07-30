## US-MINES-API DOCUMENTATION

The Domain is https://us-mines-api.herokuapp.com

### GET REQUEST

#### AVAILABLE ROUTES

1. Get the list of all available materials

https://us-mines-api.herokuapp.com/mines/materials

2. Get mines by material and gps coordinates within a particular radius

The general format is:

https://us-mines-api.herokuapp.com/mines/{material}/@{longitude},{latitude},{radius}

Results will be sorted based on distance, from nearest to furthest.

Validation:

Material cannot contain non-characters and should be separated by "+".

The longitude, latitude, and radius are separated by a comma.

Longitude must be negative and latitude and radius must be larger than 0.

Longitude and latitude should also be in their acceptable range (-180 to 180, -90 to 90, respectively)

Examples:

Get sand and gravel mines within a 40-mile-radius of point -82 longitude, 30 latitude
https://us-mines-api.herokuapp.com/mines/sand+and+gravel/@-87,30,40

Others:
http://us-mines-api.herokuapp.com/mines/sand+and+gravel/@-87.5,30.23,40
http://us-mines-api.herokuapp.com/mines/sand/@-145.5,60.23,100
http://us-mines-api.herokuapp.com/mines/limestone/@-70.5,45.23,100
http://us-mines-api.herokuapp.com/mines/crushed,+broken+limestone+nec/@-120,50,200

Tip:
Lat-long coorditates for cities in United States are in range: Latitude from 19.50139 to 64.85694 and longitude from -161.75583 to -68.01197. To catch more miles, simply increase the radius
