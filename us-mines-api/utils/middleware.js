//unknown endpoint err handler
const unknownEndpoint = (request, response) => {
	response.status(404).json({ error: 'unknown endpoint' })
}

const errorHandler = (error, request, response, next) => {
	if (error) {
		console.log(error)
		return response.status(500).json({ error: 'Internal Server Error' })
	}
	next(error)
}

module.exports = {
	unknownEndpoint,
	errorHandler,
}
