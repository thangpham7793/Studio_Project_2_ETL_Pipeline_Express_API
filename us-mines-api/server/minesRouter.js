const express = require('express')
const minesRouter = express.Router()
const routeHandlers = require('./routeHandlers')
const routeRegex = require('./routeRegex')
const cors = require('cors') //allow cross-origin-requests for certain routes

require('express-async-errors')

// GET MINES BY LATLNG (200 MILES RADIUS DEFAULT) REGARDLESS OF MATERIALS
minesRouter.get(routeRegex.minesByLatLng, cors(), routeHandlers.getMines)

// GET MINES BY LATLNG AND RADIUS REGARDLESS OF MATERIALS
minesRouter.get(
	routeRegex.minesByLatLngAndRadius,
	cors(),
	routeHandlers.getMines
)

// GET MINES BY LATLONG AND MATERIAL WITHIN A SPECIFIC RADIUS
minesRouter.get(
	routeRegex.minesByMaterialAndLatLngAndRadius,
	cors(),
	routeHandlers.getMines
)

// GET MINES BY LATLONG AND MATERIAL IN 200 MILES RADIUS (default)
minesRouter.get(
	routeRegex.minesByMaterialAndLatLng,
	cors(),
	routeHandlers.getMines
)

// GET ONE MINE BY ID
minesRouter.get(routeRegex.mineById, routeHandlers.getOneById)

// GET ALL AVAILABLE MATERIALS
minesRouter.get('/materials', routeHandlers.getMaterials)

// WELCOME ROUTE
minesRouter.get('/', (request, response) => {
	response.status(200).json({
		message: '<h1>Welcome to the US Mines API Service</h1>',
	})
})

module.exports = minesRouter
