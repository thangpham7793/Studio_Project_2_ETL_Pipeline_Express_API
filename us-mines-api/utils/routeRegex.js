const minesByMaterialAndLatLng =
	// '/:material([a-zA-Z-_+]{1,})/@:lng(-\\d+),:lat(\\d+),:radius(\\d+)'
	// '/:material([a-zA-Z-_+]{1,})/@:lng(-\\d+\\.?\\d*),:lat(\\d+\\.?\\d*),:radius(\\d+\\.?\\d*)'
	'/:material([a-zA-Z-_+]{1,})/@:lng(-\\d+.?\\d*),:lat(\\d+.?\\d*),:radius(\\d+.?\\d*)'
module.exports = {
	minesByMaterialAndLatLng,
}
