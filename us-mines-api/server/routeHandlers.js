const callbacks = require('../utils/callbacks')
const queryMaker = require('../utils/queryMaker')
const client = require('./client')

//global collection to share through each handler
const db = client.db('us-mines-locations')
const collection = db.collection('msha')

//can have a look up table depending on the method use as well
function getRequestHandlerFactory(
	queryHandler,
	projectionMaker,
	queryOperation
) {
	return async function (userInputObject) {
		const filter = queryHandler(userInputObject)
		//NOTE: business logic here (what to show)
		//alternative syntax collection.find({}).project({a:1})
		const projection = projectionMaker([
			'_id',
			'current_mine_name',
			'primary_sic',
			'primary_canvass',
			'secondary_sic',
			'current_controller_name',
			'current_operator_name',
			'directions_to_mine',
			'nearest_town',
			'location',
		])
		console.log(filter, projection)
		let result
		try {
			result = await collection[queryOperation](filter, {
				projection: projection,
			}).toArray()
			return result
		} catch (error) {
			console.error(error)
		}
	}
}

const findNearByMinesWithinRadius = getRequestHandlerFactory(
	queryMaker.findNearByMinesWithin,
	queryMaker.projectionMaker,
	'find'
)

const getAllMaterials = async () => {
	let primarySic, secondarySic, allMaterials
	try {
		primarySic = await collection.distinct('primary_sic')
		secondarySic = await collection.distinct('secondary_sic')
		allMaterials = [...primarySic, ...secondarySic]
		const distinctMaterials = Array.from(new Set(allMaterials))
		//FIXME: secondary_sic contains some unwanted materials though
		return distinctMaterials
	} catch (error) {
		console.log(error)
	}
}

module.exports = {
	findNearByMinesWithinRadius,
	getAllMaterials,
}

//TODO: add redis (using HM hashmap to cache results + testing)
//TODO: add pagination ? (points will show on the map, but not everything will be shown on the side bar)
