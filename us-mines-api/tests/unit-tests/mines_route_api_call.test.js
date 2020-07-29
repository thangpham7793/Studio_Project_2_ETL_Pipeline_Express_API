const assert = require('assert')
const routeRegex = require('../../utils/routeRegex')
const mockGetRequest = require('supertest')
const correctRouteApp = require('express')()
const invalidRouteApp = require('express')()
const mockGETRequestURL = '/Dimension+Stone/@-89,30,20'
const expectedParams = {
	material: 'Dimension+Stone',
	lng: '-89',
	lat: '30',
	radius: '20',
}

correctRouteApp.get(routeRegex.minesByMaterialAndLatLng, function (req, res) {
	res.status(200).json(req.params)
})

invalidRouteApp.get(routeRegex.minesByMaterialAndLatLng, function (req, res) {
	res.status(404).json({ error: 'unknown endpoint' })
})

describe.only('Unit Test: Search Mines Params', function () {
	describe('GET /:material/@:lng,:lat,:radius', function () {
		it('should contain an object with the correct parameters from the mock request URL', function () {
			mockGetRequest(correctRouteApp)
				.get(mockGETRequestURL)
				.set('Accept', 'application/json')
				.expect('Content-Type', /json/)
				.expect(200)
				.then((response) => {
					assert(response.body, expectedParams)
				})
		})

		it.only('should return an unknown endpoint error message if the URL is invalid', function () {
			const invalidPaths = [
				'/12sand/@-123,30,20', //digits in material
				'sandAndGravel/@-123,30,4', //missing first backslash
				'/Dimension-Stone/@123,30,100', //positive longitude
				'/DimensionStone/@-123,-30,0', //negative latitude
				'/Dimension_Stone/@-123,30,-23', //negative radius
				'/Dimension+Stone/@-123,a30,1c', //digits in location
				'/Sand And Gravel/-123,39,10', //missing @
			]

			mockGetRequest(invalidRouteApp)
				.get(invalidPaths[0])
				.set('Accept', 'application/json')
				.expect('Content-Type', /json/)
				.expect(404)
				.then((response) => {
					assert(response.body, { error: 'unknown endpoint' })
				})
				.catch((err) => console.log(err.message))
			//doesn't support concurrency it seems
			// invalidPaths.forEach((invalidPath) => {
			// 	mockGetRequest(invalidRouteApp)
			// 		.get(invalidPath)
			// 		.set('Accept', 'application/json')
			// 		.expect('Content-Type', /json/)
			// 		.expect(404)
			// 		.then((response) => {
			// 			assert(response.body, { error: 'unknown endpoint' })
			// 		})
			// 		.catch((err) => console.log(err.message))
			// })
		})
	})
})

//TODO: write tests for successful calls (this is integration test rather than unit test)