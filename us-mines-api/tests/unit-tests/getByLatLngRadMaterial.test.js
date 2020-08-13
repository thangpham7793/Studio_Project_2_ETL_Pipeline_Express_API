const assert = require('assert')
const { parsePath } = require('../testUtils')
const longitudePattern = '/@:lng(-\\d+.?\\d*)'
const materialPattern = '/:material([a-zA-Z-_+]{1,})'
const fullPattern = require('../../controller/routeRegex')
	.minesByMaterialAndLatLng

describe('Unit Test: GET Mines by Material and LatLng Path Regex', () => {
	describe(`the regex path "/@:lng(-\\d+)"`, () => {
		it('should return null when the path begins with a non-digit character', () => {
			const path = '@/a123'
			const res = parsePath(longitudePattern, path)
			assert.equal(null, res)
		})

		it("should return null when there's positive number", () => {
			const path = '/@123'
			const res = parsePath(longitudePattern, path)
			assert.equal(null, res)
		})

		it('should return null when a backslash is missing', () => {
			const path = '@-123'
			const res = parsePath(longitudePattern, path)
			assert.equal(null, res)
		})

		it('should return a negative number when the path contains a negative number', () => {
			const path = '/@-123'
			const res = parsePath(longitudePattern, path)
			// console.log(res);
			assert.equal(true, res.includes(path))
		})

		it('should return null when the path contains a character despite the valid number', () => {
			const paths = ['/@a-123', '/@-1bdc23', 'a/@-123', '/@-123bc']
			paths.forEach((path) => {
				assert.equal(null, parsePath(longitudePattern, path))
			})
		})

		it('should return a decimal when a decimal is used', () => {
			const path = '/@-123.85'
			const res = parsePath(longitudePattern, path)
			assert.equal(true, res.includes(path))
		})
	})

	describe(`the regex for material ${materialPattern}`, () => {
		it('should return only characters from the result regardless of case and delimiter', () => {
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
				const res = parsePath(materialPattern, material)
				//console.log('The result is ' + res + '\n')
				assert.equal(true, res.includes(material))
			})
		})

		it("should return null if there's non-alphabetic input", () => {
			const materials = [
				'/material=sand123',
				'/material=123sand',
				'/material=sa23nd',
				'/material=12sand34',
				'/material=12sand%=?',
			]
			materials.forEach((material) => {
				const res = parsePath(materialPattern, material)
				//console.log('The result is ' + res + '\n')
				assert.equal(null, res)
			})
		})
	})

	describe(`the regex for the full path${fullPattern}`, () => {
		it('should return correct urls regardless of case and delimiter', () => {
			const paths = [
				'/sand/@-123.234,30.5',
				'/sandAndGravel/@-123,30.54',
				'/Dimension-Stone/@-123.34,30',
				'/DimensionStone/@-123.452,30.54646923942',
				'/Dimension_Stone/@-123.435329424932,30.54683249329',
				'/Dimension+Stone/@-123,30',
				'/gravel/@-87,30',
			]
			paths.forEach((path) => {
				const res = parsePath(fullPattern, path)
				assert.equal(true, res.includes(path))
			})
		})

		it('should return null when any of the params is invalid', () => {
			const invalidPaths = [
				'/12sand/@-123,30', //digits in material
				'sandAndGravel/@-123,30', //missing first backslash
				'/Dimension-Stone/@123,30', //positive longitudePattern
				'/DimensionStone/@-123,-30', //negative latitude
				'/Dimension+Stone/@-123,a30', //digits in location
				'/Sand And Gravel/-123,39', //missing @
			]
			invalidPaths.forEach((invalidPath) => {
				const res = parsePath(fullPattern, invalidPath)
				assert.equal(null, res)
			})
		})
	})
})

//https://developers.google.com/web/updates/2016/01/urlsearchparams
//https://jordankasper.com/a-reintroduction-to-express.js-routes/
