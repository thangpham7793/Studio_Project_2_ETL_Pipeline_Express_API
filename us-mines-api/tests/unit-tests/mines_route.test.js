const assert = require('assert')
const parsePath = require('./testUtils')
const longitude = '/@:lng(-\\d+)'
const materialParam = '/:material([a-zA-Z-_+]{1,})'

//following Google (e.g. /dimension+stone/@-87.3432,45.123123,20)
const fullPath =
	'/:material([a-zA-Z-_+]{1,})/@:lng(-\\d+),:lat(\\d+),:radius(\\d+)'

describe('Unit Test: Mines Route Path Regex', function () {
	describe(`the regex half path "/@:lng(-\\d+)"`, function () {
		it('should return null when the path begins with a non-digit character', function () {
			const path = '@/a123'
			const res = parsePath(longitude, path)
			assert.equal(null, res)
		})

		it("should return null when there's positive number", function () {
			const path = '/@123'
			const res = parsePath(longitude, path)
			assert.equal(null, res)
		})

		it('should return null when a backslash is missing', function () {
			const path = '@-123'
			const res = parsePath(longitude, path)
			assert.equal(null, res)
		})

		it('should return a negative number when the path contains a negative number', function () {
			const path = '/@-123'
			const res = parsePath(longitude, path)
			// console.log(res);
			assert.equal(true, res.includes(path))
		})

		it('should return null when the path contains a character despite the valid number', function () {
			const paths = ['/@a-123', '/@-1bdc23', 'a/@-123', '/@-123bc']
			paths.forEach((path) => {
				assert.equal(null, parsePath(longitude, path))
			})
		})
	})

	describe(`the regex for material ${materialParam}`, function () {
		it('should return only characters from the result regardless of case and delimiter', function () {
			const materials = [
				'/sand',
				'/Sand',
				'/SAND-and-Gravel',
				'/sand-and_Gravel',
				'/sandAndGravel',
				'/Dimension-Stone',
				'/Dimension+Stone',
			]
			materials.forEach((material) => {
				const res = parsePath(materialParam, material)
				console.log('The result is ' + res + '\n')
				assert.equal(true, res.includes(material))
			})
		})

		it("should return null if there's non-alphabetic input", function () {
			const materials = [
				'/material=sand123',
				'/material=123sand',
				'/material=sa23nd',
				'/material=12sand34',
				'/material=12sand%=?',
			]
			materials.forEach((material) => {
				const res = parsePath(materialParam, material)
				console.log('The result is ' + res + '\n')
				assert.equal(null, res)
			})
		})
	})

	describe(`the regex for the full path${fullPath}`, function () {
		it('should return correct urls regardless of case and delimiter', function () {
			const paths = [
				'/sand/@-123,30,20',
				'/sandAndGravel/@-123,30,4',
				'/Dimension-Stone/@-123,30,100',
				'/DimensionStone/@-123,30,0',
				'/Dimension_Stone/@-123,30,23',
				'/Dimension+Stone/@-123,30,1',
			]
			paths.forEach((path) => {
				const res = parsePath(fullPath, path)
				assert.equal(true, res.includes(path))
			})
		})

		it('should return null when any of the params is invalid', function () {
			const invalidPaths = [
				'/12sand/@-123,30,20', //digits in material
				'sandAndGravel/@-123,30,4', //missing first backslash
				'/Dimension-Stone/@123,30,100', //positive longitude
				'/DimensionStone/@-123,-30,0', //negative latitude
				'/Dimension_Stone/@-123,30,-23', //negative radius
				'/Dimension+Stone/@-123,a30,1c', //digits in location
				'/Sand And Gravel/-123,39,10', //missing @
			]
			invalidPaths.forEach((invalidPath) => {
				const res = parsePath(fullPath, invalidPath)
				assert.equal(null, res)
			})
		})
	})
})

//https://developers.google.com/web/updates/2016/01/urlsearchparams
//https://jordankasper.com/a-reintroduction-to-express.js-routes/
