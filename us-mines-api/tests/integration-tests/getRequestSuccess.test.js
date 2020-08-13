const assert = require('assert')
const request = require('supertest')
const client = require('../../mongodb/client')
const { isEmpty } = require('../testUtils')

//NOTE: should run at least 2 or 3 tests together in case of the client closes too early. Should also run the test suite alone

//global var to save the app after connecting to database
let app

describe('Connecting to MongoDB', () => {
	//https://mochajs.org/#hooks
	before((done) => {
		client.connect((err) => {
			if (err) {
				console.log('Failed to connect to Mongodb Atlas: ', err.message)
				return
			} else {
				console.log('\nSuccessfully connect to Mongodb Atlas')
				//only initialize express app when connected to database
				app = require('../../app')
				done()
			}
		})
	})

	//close connection after all tests
	after((done) => {
		console.log('Closing Client!')
		client.close()
		done()
	})

	describe('Integration Test: GET Routes', () => {
		describe('GET /', () => {
			it('should return a welcome message', () => {
				return request(app)
					.get('/')
					.expect('Content-Type', 'application/json; charset=utf-8')
					.expect(200)
					.expect((response) => {
						assert.equal(
							response.body.message,
							'Welcome to the US Mines & Landfills API Service'
						)
					})
			})
		})

		describe('GET /mines', () => {
			it('should return a welcome message', () => {
				return request(app)
					.get('/mines')
					.expect('Content-Type', 'application/json; charset=utf-8')
					.expect(200)
					.expect((response) => {
						assert.equal(
							response.body.message,
							'Welcome to the US Mines API Service'
						)
					})
			})
		})

		describe('GET /landfills', () => {
			it('should return a welcome message', () => {
				return request(app)
					.get('/landfills')
					.expect('Content-Type', 'application/json; charset=utf-8')
					.expect(200)
					.expect((response) => {
						assert.equal(
							response.body.message,
							'Welcome to the US Landfills API Service'
						)
					})
			})
		})

		describe('GET /mines/materials', () => {
			it('should return an array of all available materials that contain "sand and gravel"', () => {
				return request(app)
					.get('/mines/materials')
					.expect('Content-Type', 'application/json; charset=utf-8')
					.expect(200)
					.expect((response) => {
						assert(true, Array.isArray(response.body.materials))
						assert(true, response.body.materials.length > 0)
						assert(true, response.body.materials.includes('sand and gravel'))
					})
			})
		})

		describe(`GET mines or landfills`, () => {
			const validParams = [
				'/mines/@-87,30,80', //all materials default radius
				'/mines/@-145.5,60.23,50', //all materials custom radius
				'/mines/sand+and+gravel/@-87.5,30.23', //one material with default radius
				'/mines/sand+and+gravel/@-87.5,30.23,120', //one material with custom radius
				'/landfills/@-100,35',
				'/landfills/@-102,36.23,50',
			]
			validParams.forEach((params) => {
				it(`should return status 200 when params are valid ${params}`, () => {
					return request(app)
						.get(params)
						.expect('Content-Type', 'application/json; charset=utf-8')
						.expect(200)
				})
			})

			const validId = [
				'/mines/5f326ec5903f3e0d204c26da',
				'/landfills/5f326ddb903f3e0d204bd8ff',
			]
			validId.forEach((id) => {
				it(`should return status 200 and a result object when id are valid ${id}`, () => {
					return request(app)
						.get(id)
						.expect('Content-Type', 'application/json; charset=utf-8')
						.expect(200)
						.expect((response) => {
							//compare the returned id with the received id
							assert.equal(id.split('/').pop(), response.body._id)
							//test if the result object contains information
							assert.equal(false, isEmpty(response.body))
						})
				})
			})
		})
	})
})
