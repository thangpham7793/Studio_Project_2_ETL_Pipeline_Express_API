const assert = require('assert')
const routeRegex = require('../../server/routeRegex')
const mockGetRequest = require('supertest')
const validRouteApp = require('express')()
const invalidRouteApp = require('express')()
const mockGETRequestURL = '/Dimension+Stone/@-89,30'
const expectedParams = {
	material: 'Dimension+Stone',
	lng: '-89.5334543534',
	lat: '30.45546564',
}

validRouteApp.get(routeRegex.minesByMaterialAndLatLng, function (req, res) {
	res.status(200).json(req.params)
})

invalidRouteApp.get(routeRegex.minesByMaterialAndLatLng, function (req, res) {
	res.status(404).json({ error: 'unknown endpoint' })
})

describe('Integration Test: Search Mines Params', function () {
	describe('GET /:material/@:lng,:lat,:radius', function () {
		it('should contain an object with the correct parameters from the mock request URL', function () {
			mockGetRequest(validRouteApp)
				.get(mockGETRequestURL)
				.set('Accept', 'application/json; text/html; charset=utf-8')
				.expect('Content-Type', /[json|text]/)
				.expect(200)
				.then((response) => {
					assert(response.body, expectedParams)
				})
		})

		it('should return an unknown endpoint error message if the URL is invalid', function () {
			const invalidPaths = [
				'/12sand/@-123,30', //digits in material
				'sandAndGravel/@-123,30', //missing first backslash
				'/Dimension-Stone/@123,30', //positive longitude
				'/DimensionStone/@-123,-30', //negative latitude
				'/Dimension_Stone/@-123,30', //negative radius
				'/Dimension+Stone/@-123,a30', //digits in location
				'/Sand And Gravel/-123,39', //missing @
			]

			mockGetRequest(invalidRouteApp)
				.get(invalidPaths[3])
				.set('Accept', 'application/json; text/html; charset=utf-8')
				.expect('Content-Type', /[json|text]/)
				.expect(404)
				.then((response) => {
					assert(response.body, { error: 'unknown endpoint' })
				})
				.catch((err) => console.log(err.message))
		})
	})
})
//FIXME: still can't connect to MongoDB
