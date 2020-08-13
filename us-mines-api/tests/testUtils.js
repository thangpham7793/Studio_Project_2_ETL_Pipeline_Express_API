const { pathToRegexp } = require('path-to-regexp')

function parsePath(pattern, input) {
	const regexp = pathToRegexp(pattern)
	return regexp.exec(input)
}

function isEmpty(obj) {
	for (let prop in obj) {
		return false
	}
	return true
}

module.exports = { parsePath, isEmpty }
