//global collection to share through each handler
const client = require('./client')
const config = require('../utils/config')
const db = client.db(config.MONGODB_NAME)
const collection = db.collection(config.MONGODB_COLLECTION)

//optional callbacks to process returned json documents
const callbacks = require('./callbacks')
const queryMakers = require('./queryMakers')
const logger = require('../utils/logger')
const ObjectID = require('mongodb').ObjectID

const findMineById = async (id) => {
	const o_id = new ObjectID(id)

	//NOTE: business logic here (what to show)
	//alternative syntax collection.find({}).project({a:1})
	const targetFieldsObject = queryMakers.projectionMaker([
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
		result = await collection.findOne(
			{ _id: o_id },
			{ projection: targetFieldsObject }
		)
		//can add callback here to process results
		return result
	} catch (error) {
		logger.error(error)
	}
}

const findAllMaterials = async () => {
	let primarySic, secondarySic, allMaterials
	if (cachedResponse)
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

//can have a look up table depending on the method use as well
const findMinesByMaterialLatLngRadius = async (userInputObject) => {
	const filter = queryMakers.minesByLatLngMaterialRadius(userInputObject)

	//NOTE: business logic here (what to show)
	//alternative syntax collection.find({}).project({a:1})
	const targetFieldsObject = queryMakers.projectionMaker([
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
		result = await collection
			.find(filter, {
				projection: targetFieldsObject,
			})
			.toArray()
		return result
	} catch (error) {
		logger.error(error)
	}
}

module.exports = {
	findMinesByMaterialLatLngRadius,
	findMineById,
	findAllMaterials,
}
