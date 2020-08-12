/**
 * Callback functions that process query results
 * @param {array} resArr
 */

//for example, remove the id of each returned document
function removeId(resArr) {
	return resArr.map((doc) => {
		delete doc._id
		return doc
	})
}

function processMinesResults(res) {
	//TODO: how and where to add gzip
	console.log('Processing done, returning result')
	return removeId(res)
}

module.exports = {
	processMinesResults,
}
