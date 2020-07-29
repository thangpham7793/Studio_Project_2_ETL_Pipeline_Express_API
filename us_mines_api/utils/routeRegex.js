const minesByMaterialAndLatLng =
	'/:material([a-zA-Z-_+]{1,})/@:lng(-\\d+),:lat(\\d+),:radius(\\d+)'

module.exports = {
	minesByMaterialAndLatLng,
}
