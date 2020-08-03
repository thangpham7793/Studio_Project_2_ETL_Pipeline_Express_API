const minesByMaterialAndLatLng =
	//following Google (e.g. /dimension+stone/@-87.3432,45.123123,20)
	'/:material([a-zA-Z-_+,]{1,})/@:lng(-\\d+.?\\d*),:lat(\\d+.?\\d*)'

//id must be 24-char long and contains only alphanumeric characters
const mineById = '/:id(\\w{24})'

module.exports = {
	minesByMaterialAndLatLng,
	mineById,
}

//FIXME: need to make radius optional rather than removing it completely
