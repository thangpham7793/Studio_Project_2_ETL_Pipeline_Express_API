const express = require('express')
const minesRouter = express.Router()
const routeHandlers = require('../server/routeHandlers')
const routeRegex = require('../server/routeRegex')
const cors = require('cors') //allow cross-origin-requests for certain routes

require('express-async-errors')

// GET MINES BY LATLONG AND MATERIAL WITHIN A SPECIFIC RADIUS
minesRouter.get(
	routeRegex.minesByMaterialAndLatLngWithRadius,
	cors(),
	routeHandlers.getMinesByMaterialAndLatLng
)

// GET MINES BY LATLONG AND MATERIAL IN 200 MILES RADIUS (default)
minesRouter.get(
	routeRegex.minesByMaterialAndLatLng,
	cors(),
	routeHandlers.getMinesByMaterialAndLatLng
)

// GET ONE MINE BY ID
minesRouter.get(routeRegex.mineById, routeHandlers.getOneMineById)

// GET ALL MINES REGARDLESS OF MATERIALS BY LATLNG (200 MILES RADIUS DEFAULT)

minesRouter.get(
	routeRegex.allMinesByLatLng,
	cors(),
	routeHandlers.getAllMinesByLatLng
)

minesRouter.get('/', (request, response) => {
	response.status(200).json({
		message: '<h1>Welcome to the US Mines API Service</h1>',
	})
})

minesRouter.get('/materials', routeHandlers.getMaterials)

module.exports = minesRouter
