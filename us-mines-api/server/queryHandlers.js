//global collection to share through each handler
const client = require('./client')
const db = client.db('us-mines-locations')
const collection = db.collection('msha')

//optional callbacks to process returned json documents
const callbacks = require('./callbacks')
const queryMaker = require('./queryMaker')
const logger = require('../utils/logger')
const ObjectID = require('mongodb').ObjectID

//can have a look up table depending on the method use as well
const findMilesByMaterialAndLatLng = async (userInputObject) => {
	const filter = queryMaker.findNearByMinesWithin(userInputObject)

	//NOTE: business logic here (what to show)
	//alternative syntax collection.find({}).project({a:1})
	const targetFieldsObject = queryMaker.projectionMaker([
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

const findMineById = async (id) => {
	const o_id = new ObjectID(id)

	//NOTE: business logic here (what to show)
	//alternative syntax collection.find({}).project({a:1})
	const targetFieldsObject = queryMaker.projectionMaker([
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
		//can add callback here
		return result
	} catch (error) {
		logger.error(error)
	}
}

const findAllMaterials = async () => {
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

const findMilesByLatLng = async (userInputObject) => {
	const filter = queryMaker.allMinesByLatLng(userInputObject)

	//NOTE: business logic here (what to show)
	//alternative syntax collection.find({}).project({a:1})
	const targetFieldsObject = queryMaker.projectionMaker([
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
	findMilesByLatLng,
	findMilesByMaterialAndLatLng,
	findMineById,
	findAllMaterials,
}
