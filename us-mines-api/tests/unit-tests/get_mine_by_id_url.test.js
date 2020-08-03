const assert = require('assert')
const pattern = require('../../server/routeRegex').mineById
const parsePath = require('./testUtils')

describe('Unit Test: GET Mine by Id Regex Path', () => {
	it('should return the id string when there are 25 letters or numbers in total including the backslash', () => {
		const validPaths = [
			'/5f1d249e0e492f317de09918',
			'/5f1d24930e492f317de07425',
		]
		validPaths.forEach((path) => {
			const result = parsePath(pattern, path)
			assert.equal(true, result.includes(path))
			assert.equal(25, result[0].length)
		})
	})

	it('should return null if the id string is more or less than 24 characters', () => {
		const inValidPaths = [
			'/5f1d249e0e492f317de0',
			'/5f1d24417de07425asa45ksjh42',
		]
		inValidPaths.forEach((path) => {
			const result = parsePath(pattern, path)
			assert.equal(null, result)
		})
	})

	it('should return null if the string contains invalid characters', () => {
		const inValidPaths = [
			'/5f1d249e0e492f317de0991?',
			'/5f1d24930e492f317de0742-',
			'/5f1d24930e492f317de0742;',
			'/5f1d24930)492f317de0742-',
			'/5f1d24930e492./(17de0742',
		]
		inValidPaths.forEach((path) => {
			const result = parsePath(pattern, path)
			assert.equal(null, result)
		})
	})

	it('should return null if the string contains invalid characters', () => {
		const inValidPaths = [
			'/=f1d249e0e492f317de0991?',
			'/5f1d%4930e492f317de0742-',
			'/5f1d24930e492f317de0742;',
			'/5f1d@4930)492f317de0742-',
			'/5f1d24930e492./(17de0742',
		]
		inValidPaths.forEach((path) => {
			const result = parsePath(pattern, path)
			assert.equal(null, result)
		})
	})

	it('should return null if the backslash is missing', () => {
		const inValidPaths = ['5f1d24930e492ase17de0742']
		inValidPaths.forEach((path) => {
			const result = parsePath(pattern, path)
			assert.equal(24, path.length)
			assert.equal(null, result)
		})
	})
})
