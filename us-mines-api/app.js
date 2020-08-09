const express = require('express')
const app = express()

const bodyParser = require('body-parser')

const middleware = require('./utils/middleware')
const minesRouter = require('./server/minesRouter')

//get methods from bodyParser
const { urlencoded, json } = bodyParser

//parse incoming request using bodyParser
app.use(json())
app.use(urlencoded({ extended: false }))

//welcome message for index page
app.get('/', (request, response) =>
	response
		.status(200)
		.send({ message: 'Welcome to the US Mines & Landfills API Service' })
)

//direct mines-related queries to its dedicated mini-app
app.use('/mines', minesRouter)

//handle errors
app.use(middleware.unknownEndpoint)
app.use(middleware.errorHandler)

module.exports = app
