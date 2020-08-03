const callbacks = require('../utils/callbacks')
const queryMaker = require('./queryMaker')
const client = require('./client')
const logger = require('../utils/logger')
const ObjectID = require('mongodb').ObjectID
//global collection to share through each handler
const db = client.db('us-mines-locations')
const collection = db.collection('msha')

//can have a look up table depending on the method use as well
const getRequestHandlerFactory = (queryHandler, queryOperation) => {
	return async function (userInputObject) {
		const filter = queryHandler(userInputObject)
		//NOTE: business logic here (what to show)
		//alternative syntax collection.find({}).project({a:1})
		const projection = queryMaker.projectionMaker([
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
		let result
		try {
			result = await collection[queryOperation](filter, {
				projection: projection,
			}).toArray()
			return result
		} catch (error) {
			logger.error(error)
		}
	}
}

const findMilesByMaterialAndLatLng = getRequestHandlerFactory(
	queryMaker.findNearByMinesWithin,
	'find'
)

const findMineById = async (id) => {
	const o_id = new ObjectID(id)
	const projection = queryMaker.projectionMaker([
		'_id',
		'current_mine_name',
		'primary_sic',
		'secondary_sic',
		'current_controller_name',
		'current_operator_name',
		'directions_to_mine',
		'nearest_town',
		'location',
	])
	let result
	try {
		result = await collection.findOne({ _id: o_id }, { projection: projection })
		console.log(result)
		return result
	} catch (error) {
		logger.error(error)
	}
}

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
	findMilesByMaterialAndLatLng,
	findMineById,
	getAllMaterials,
}
