const queryHandlers = require('../mongodb/queryHandlers')

/**
 * Route each GET request to its suitable query handler
 * @param {object} request
 * @param {object} response
 */

//MINES QUERY HANDLERS

const getMines = async (request, response) => {
	//let { lng, lat, material, radius } = request.params
	let { material, lng, lat, radius } = request.params

	lng = parseFloat(lng)
	lat = parseFloat(lat)
	radius = parseFloat(radius)
	//replace all non-character with a space, then split on space and filter out space and empty string before joining them
	if (material !== undefined)
		material = material
			.replace(/[^a-zA-Z,]/g, ' ')
			.split(' ')
			.filter((char) => char.indexOf(' ') === -1 && char.length > 0)
			.join(' ')

	if (lng < -180 || lng > 180 || lat < -90 || lat > 90) {
		throw new Error(
			'Longitude must be between -180 and 180. Latitude must be between -90 and 90!'
		)
	} else if (radius <= 0) {
		throw new Error('Radius must be bigger than 0!')
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

//LANDFILLS QUERY HANDLERS
const getLandfills = async (request, response) => {
	let { lng, lat, radius } = request.params

	lng = parseFloat(lng)
	lat = parseFloat(lat)
	radius = parseFloat(radius)

	if (lng < -180 || lng > 180 || lat < -90 || lat > 90) {
		throw new Error(
			'Longitude must be between -180 and 180. Latitude must be between -90 and 90!'
		)
	} else if (radius <= 0) {
		throw new Error('Radius must be bigger than 0!')
	} else {
		const params = {
			lat,
			lng,
			radius,
		}
		const result = await queryHandlers.findLandfillsByLatLngRadius(params)
		result.length > 0
			? response.status(200).json(result)
			: response.status(404).json({ message: 'No landfill found' })
	}
}

// get one record by ID, could be mine or landfill
const getOneById = async (request, response) => {
	let id = request.params.id
	const result = await queryHandlers.findById(id)
	result !== null
		? response.status(200).json(result)
		: response.status(404).json({ message: 'No site found' })
}

module.exports = {
	getMines,
	getMaterials,
	getLandfills,
	getOneById,
}
