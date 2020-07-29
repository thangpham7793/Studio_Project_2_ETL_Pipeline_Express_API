const minesByMaterialAndLatLng =
	//following Google (e.g. /dimension+stone/@-87.3432,45.123123,20)
	'/:material([a-zA-Z-_+]{1,})/@:lng(-\\d+.?\\d*),:lat(\\d+.?\\d*),:radius(\\d+.?\\d*)'
module.exports = {
	minesByMaterialAndLatLng,
}
