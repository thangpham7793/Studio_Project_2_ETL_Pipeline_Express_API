//following Google (e.g. /dimension+stone/@-87.3432,45.123123,20)
const minesByLatLng = '/@:lng(-\\d+.?\\d*),:lat(\\d+.?\\d*)'

const minesByLatLngAndRadius =
	'/@:lng(-\\d+.?\\d*),:lat(\\d+.?\\d*),:radius(\\d+.?\\d*)'

const minesByMaterialAndLatLng =
	'/:material([a-zA-Z-_+,]{3,})/@:lng(-\\d+.?\\d*),:lat(\\d+.?\\d*)'

const minesByMaterialAndLatLngAndRadius =
	'/:material([a-zA-Z-_+,]{3,})/@:lng(-\\d+.?\\d*),:lat(\\d+.?\\d*),:radius(\\d+.?\\d*)'

//id must be 24-char long and contains only alphanumeric characters
const mineById = '/:id(\\w{24})'

module.exports = {
	minesByLatLng,
	minesByLatLngAndRadius,
	minesByMaterialAndLatLng,
	minesByMaterialAndLatLngAndRadius,
	mineById,
}
