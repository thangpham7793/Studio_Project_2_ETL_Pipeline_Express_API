const express = require('express')
const landfillsRouter = express.Router()
const routeHandlers = require('./routeHandlers')
const routeRegex = require('./routeRegex')
const cors = require('cors') //allow cross-origin-requests for certain routes

require('express-async-errors')

// GET landfills BY LATLNG (200 MILES RADIUS DEFAULT)
landfillsRouter.get(
	routeRegex.landfillsByLatLng,
	cors(),
	routeHandlers.getLandfills
)

// GET landfills BY LATLNG AND RADIUS
landfillsRouter.get(
	routeRegex.landfillsByLatLngAndRadius,
	cors(),
	routeHandlers.getLandfills
)

// GET ONE landfill BY ID
landfillsRouter.get(routeRegex.landfillById, routeHandlers.getOneById)

// WELCOME ROUTE
landfillsRouter.get('/', (request, response) => {
	response.status(200).json({
		message:
			'Welcome to the US Landfills API Service. Visit "https://github.com/CGHill/Signal_Studio_Project2/tree/master/us-mines-api" for Documentation',
	})
})

module.exports = landfillsRouter
