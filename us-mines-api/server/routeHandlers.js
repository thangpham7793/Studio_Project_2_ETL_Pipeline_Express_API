const queryHandlers = require('../mongodb/queryHandlers')

//FIXME: combine all the routes into one handler?
const getMines = async (request, response) => {
	let { lng, lat, material, radius } = request.params

	lng = parseFloat(lng)
	lat = parseFloat(lat)
	radius = parseFloat(radius)
	//replace all non-character with a space, then split on space and filter out space and empty string before joining them
	if (material != undefined)
		material = material
			.replace(/[^a-zA-Z,]/g, ' ')
			.split(' ')
			.filter((char) => char.indexOf(' ') === -1 && char.length > 0)
			.join(' ')

	if (lng < -180 || lng > 180 || lat < -90 || lat > 90) {
		response.status(400).send({
			error:
				'Longitude must be between -180 and 180. Latitude must be between -90 and 90!',
		})
	} else if (radius <= 0) {
		response.status(400).send({
			error: 'Radius must be bigger than 0!',
		})
	} else {
		const params = {
			lat,
			lng,
			material,
			radius,
		}
		const result = await queryHandlers.findMinesByMaterialLatLngRadius(params)
		result.length > 0
			? response.status(200).json(result)
			: response.status(404).json({ message: 'No mine found' })
	}
}

const getMaterials = async (request, response) => {
	const allMaterials = await queryHandlers.findAllMaterials()
	allMaterials.length !== 0
		? response.status(200).json({ materials: allMaterials })
		: response.status(404).json({ message: 'No material found' })
}

const getOneMineById = async (request, response) => {
	let id = request.params.id
	const result = await queryHandlers.findMineById(id)
	result !== null
		? response.status(200).json(result)
		: response.status(404).json({ message: 'No mine found' })
}

module.exports = {
	getMines,
	getMaterials,
	getOneMineById,
}
