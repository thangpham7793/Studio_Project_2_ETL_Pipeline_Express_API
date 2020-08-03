const express = require('express')
const minesRouter = express.Router()
const routeHandlers = require('../server/routeHandlers')
const routeRegex = require('../server/routeRegex')
const cors = require('cors') //allow cross-origin-requests for certain routes

require('express-async-errors')

// GET MINES BY LATLONG WITHIN A SPECIFIC RADIUS
minesRouter.get(
	routeRegex.minesByMaterialAndLatLngWithRadius,
	cors(),
	routeHandlers.getMinesHandler
)

// GET MINES BY LATLONG IN 200 MILES RADIUS (default)
minesRouter.get(
	routeRegex.minesByMaterialAndLatLng,
	cors(),
	routeHandlers.getMinesHandler
)

// GET ONE MINE BY ID
minesRouter.get(routeRegex.mineById, routeHandlers.getOneMineHandler)

minesRouter.get('/', (request, response) => {
	response.status(200).json({
		message: '<h1>Welcome to the US Mines API Service</h1>',
	})
})

minesRouter.get('/materials', routeHandlers.getMaterialsHandler)

module.exports = minesRouter
