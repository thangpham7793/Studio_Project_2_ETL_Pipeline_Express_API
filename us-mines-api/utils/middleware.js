//unknown endpoint err handler
const unknownEndpoint = (request, response) => {
	response.status(404).json({ error: 'unknown endpoint' })
}

const errorHandler = (error, request, response, next) => {
	next(error)
}

module.exports = {
	unknownEndpoint,
	errorHandler,
}
