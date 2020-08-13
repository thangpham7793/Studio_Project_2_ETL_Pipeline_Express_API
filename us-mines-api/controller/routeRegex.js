//MINES ROUTES

//NOTE: use {0,} instead of * since it's interpreted as "anything" rather than "0 or more repetitions". https://github.com/expressjs/express/issues/2495

//following Google (e.g. /dimension+stone/@-87.3432,45.123123,20)
const minesByLatLngAndRadius =
	'/@:lng(-\\d+.?\\d{0,}),:lat(\\d+.?\\d{0,}),:radius(\\d+.?\\d{0,})'

const minesByLatLng = '/@:lng(-\\d+.?\\d{0,}),:lat(\\d+.?\\d{0,})'

const minesByMaterialAndLatLng =
	'/:material([a-zA-Z-_+,]{3,})/@:lng(-\\d+.?\\d{0,}),:lat(\\d+.?\\d{0,})'

const minesByMaterialAndLatLngAndRadius =
	'/:material([a-zA-Z-_+,]{3,})/@:lng(-\\d+.?\\d{0,}),:lat(\\d+.?\\d{0,}),:radius(\\d+.?\\d{0,})'

//id must be 24-char long and contains only alphanumeric characters
//https://docs.mongodb.com/manual/reference/method/ObjectId/
const mineById = '/:id(\\w{24})'
const landfillById = '/:id(\\w{24})'

//LANDFILLS ROUTES
const landfillsByLatLng = '/@:lng(-\\d+.?\\d{0,}),:lat(\\d+.?\\d{0,})'

const landfillsByLatLngAndRadius =
	'/@:lng(-\\d+.?\\d{0,}),:lat(\\d+.?\\d{0,}),:radius(\\d+.?\\d{0,})'

module.exports = {
	minesByLatLng,
	minesByLatLngAndRadius,
	minesByMaterialAndLatLng,
	minesByMaterialAndLatLngAndRadius,
	mineById,
	landfillsByLatLng,
	landfillsByLatLngAndRadius,
	landfillById,
}
