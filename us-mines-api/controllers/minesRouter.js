const express = require('express')
const minesRouter = express.Router()
const routeHandlers = require('../server/routeHandlers')
const routeRegex = require('../server/routeRegex')

require('express-async-errors')

// GET MINES BY LATLONG IN 200 MILES RADIUS
minesRouter.get(
	routeRegex.minesByMaterialAndLatLng,
	async (request, response) => {
		console.log(request.params)
		let { lng, lat, material } = request.params

		lng = parseFloat(lng)
		lat = parseFloat(lat)
		//replace all non-character with a space, then split on space and filter out space and empty string before joining them
		material = material
			.replace(/[^a-zA-Z,]/g, ' ')
			.split(' ')
			.filter((char) => char.indexOf(' ') === -1 && char.length > 0)
			.join(' ')

		if (lng < -180 || lng > 180 || lat < -90 || lat > 90) {
			response.status(400).send({
				error: 'Invalid latitude or longitude!',
			})
		} else {
			const params = {
				lat,
				lng,
				material,
			}
			const result = await routeHandlers.findMilesByMaterialAndLatLng(params)
			result.length > 0
				? response.status(200).json(result)
				: response.status(404).json({ message: 'No mine found' })
		}
	}
)

// GET ONE MINE BY ID

minesRouter.get(routeRegex.mineById, async (request, response) => {
	let id = request.params.id
	const result = await routeHandlers.findMineById(id)
	result !== null
		? response.status(200).json(result)
		: response.status(404).json({ message: 'No mine found' })
})

minesRouter.get('/', (request, response) => {
	response.status(200).json({
		message: '<h1>Welcome to the US Mines API Service</h1>',
	})
})

minesRouter.get('/materials', async (request, response) => {
	const allMaterials = await routeHandlers.getAllMaterials()
	allMaterials.length !== 0
		? response.status(200).json({ materials: allMaterials })
		: response.status(404).json({ message: 'No material found' })
})

// Lat-long coorditates for cities in United States are in range: Latitude from 19.50139 to 64.85694 and longitude from -161.75583 to -68.01197. (so longitude must be negative)
// ? denotes optional expression, so that's probably why some of the routes has them

module.exports = minesRouter
