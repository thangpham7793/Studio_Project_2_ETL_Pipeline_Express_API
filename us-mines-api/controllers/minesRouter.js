const express = require('express')
const minesRouter = express.Router()
const routeHandlers = require('../server/routeHandlers')
const routeRegex = require('../utils/routeRegex')

require('express-async-errors')
//  TODO: how to throttle requests?

minesRouter.get(
	routeRegex.minesByMaterialAndLatLng,
	async (request, response) => {
		let { lng, lat, material, radius } = request.params

		lng = parseFloat(lng)
		lat = parseFloat(lat)
		radius = parseFloat(radius)
		material = material
			.replace(/[^a-zA-Z]/g, ' ')
			.split(' ')
			.filter((char) => char.indexOf(' ') === -1 && char.length > 0)
			.join(' ')

		if (lng < -180 || lng > 180 || lat < -90 || lat > 90) {
			response.status(400).send({
				message: 'Invalid latitude or longitude!',
			})
		} else if (radius <= 0) {
			response.status(400).send({ message: 'Radius must be bigger than 0' })
		} else {
			const params = {
				lat,
				lng,
				material,
				radius,
			}
			const result = await routeHandlers.findNearByMinesWithinRadius(params)
			console.log(result)
			response.status(200).json(result)
		}
	}
)

minesRouter.get('/', (request, response) => {
	response.status(200).json({
		message: '<h1>Welcome to the US Mines API Service</h1>',
	})
})

minesRouter.get('/materials', async (request, response) => {
	const allMaterials = await routeHandlers.getAllMaterials()
	response.status(200).json({ materials: allMaterials })
})

// Lat-long coorditates for cities in United States are in range: Latitude from 19.50139 to 64.85694 and longitude from -161.75583 to -68.01197. (so longitude must be negative)
// ? denotes optional expression, so that's probably why some of the routes has them

module.exports = minesRouter
