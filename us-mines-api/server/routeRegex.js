const allMinesByLatLng = '/@:lng(-\\d+.?\\d*),:lat(\\d+.?\\d*)'

const minesByMaterialAndLatLng =
	//following Google (e.g. /dimension+stone/@-87.3432,45.123123,20)
	'/:material([a-zA-Z-_+,]{3,})/@:lng(-\\d+.?\\d*),:lat(\\d+.?\\d*)'

const minesByMaterialAndLatLngWithRadius =
	'/:material([a-zA-Z-_+,]{3,})/@:lng(-\\d+.?\\d*),:lat(\\d+.?\\d*),:radius(\\d+.?\\d*)'

//id must be 24-char long and contains only alphanumeric characters
const mineById = '/:id(\\w{24})'

module.exports = {
	allMinesByLatLng,
	minesByMaterialAndLatLng,
	minesByMaterialAndLatLngWithRadius,
	mineById,
}

//FIXME: need to make radius optional rather than removing it completely
