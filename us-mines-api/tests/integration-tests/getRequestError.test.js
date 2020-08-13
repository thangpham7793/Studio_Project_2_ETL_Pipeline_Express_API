const assert = require('assert')
const request = require('supertest')
const client = require('../../mongodb/client')

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
		describe('Handling Invalid GET Params', () => {
			const invalidParams = [
				'/mines/@-230,40', //longitude out of range
				'/mines/@-130,300', //latitude out of range
				'/mines/@-120,40,0', //zero radius
				'/landfills/@-230,40', //simiar but for landfills route
				'/landfills/@-130,300',
				'/landfills/@-120,40,0',
			]
			invalidParams.forEach((param) => {
				it(`should return 400 error when params are invalid ${param}`, () => {
					return request(app)
						.get(param)
						.expect('Content-Type', 'application/json; charset=utf-8')
						.expect(400)
				})
			})

			const hasInvalidCharId = [
				'/mines/5f326dd?903f3e0d204bd8c%', //both contains non-alphanumeric chars
				'/landfills/5f326dd?903f3e0d204^d8c%',
			]
			hasInvalidCharId.forEach((id) => {
				it(`should return 400 error when id contains non-alphanumeric char: ${id}`, () => {
					return request(app)
						.get(id)
						.expect('Content-Type', 'application/json; charset=utf-8')
						.expect(400)
						.expect((response) => {
							assert.equal(
								response.body.error,
								'Malformatted or Missing Parameters!'
							)
						})
				})
			})

			const invalidLengthId = [
				'/mines/5f326d903f304b', //too short
				'/landfills/5f326dd903f3e0d22adamscsqwe', //too long
			]
			invalidLengthId.forEach((id) => {
				it(`should return 400 error when id is too short or too long: ${id}`, () => {
					return request(app)
						.get(id)
						.expect('Content-Type', 'application/json; charset=utf-8')
						.expect(400)
						.expect((response) => {
							assert.equal(
								response.body.error,
								'Malformatted or Missing Parameters!'
							)
						})
				})
			})

			let malformattedId = '/mines/342dssfanasmmswqweq432sd'
			it(`should return 400 error when id is not properly formatted even with the correct length: ${malformattedId}`, () => {
				return request(app)
					.get(malformattedId)
					.expect('Content-Type', 'application/json; charset=utf-8')
					.expect(400)
					.expect((response) => {
						assert.equal(
							response.body.error,
							'Argument passed in must be a single String of 12 bytes or a string of 24 hex characters'
						)
					})
			})
		})
	})
})
