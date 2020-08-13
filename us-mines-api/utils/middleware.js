//handle invalid params
const errorHandler = (error, request, response, next) => {
	if (error.message) {
		switch (error.message) {
			case 'Longitude must be between -180 and 180. Latitude must be between -90 and 90!':
				return response.status(400).json({ error: error.message })
			case 'Radius must be bigger than 0!':
				return response.status(400).json({ error: error.message })
			default:
				return response.status(500).json({ error: 'Internal Server Error' })
		}
	} else {
		next(error)
	}
}

//unknown endpoint err handler (the last errorHandler)
const unknownEndpoint = (request, response, next) => {
	if (
		//check if the request hits the correct available routes
		request.url.startsWith('/mines') ||
		request.url.startsWith('/landfills')
	) {
		//if yes, return a custom error message for the search params
		response.status(400).json({ error: `Malformatted or Missing Parameters!` })
	} else {
		response.status(404).json({ error: 'unknown endpoint' })
	}
}
module.exports = {
	unknownEndpoint,
	errorHandler,
}
