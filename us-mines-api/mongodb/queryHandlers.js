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

/**
 * The below functions executes queries against the database and return results
 * as either an array or object that will be processed by their route handlers.
 * @param {*}
 */

// this can be used to find any facility type
const findById = async (id) => {
	const o_id = new ObjectID(id)

	//NOTE: business logic here (what to show)
	//alternative syntax collection.find({}).project({a:1})
	const targetFieldsObject = queryMakers.projectionMaker([
		'_id',
		'site_name',
		'primary_sic',
		'secondary_sic',
		'controller',
		'operator',
		'driving_directions',
		'nearest_town_or_city',
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
	try {
		//get all distinct materials from primary-sic and secondary-sic fields
		primarySic = await collection.distinct('primary_sic')
		secondarySic = await collection.distinct('secondary_sic')
		allMaterials = [...primarySic, ...secondarySic]

		//remove duplicates by creating a set
		const distinctMaterials = Array.from(new Set(allMaterials))

		//FIXME: secondary_sic contains some unwanted materials
		return distinctMaterials
	} catch (error) {
		console.log(error)
	}
}

const findMinesByMaterialLatLngRadius = async (userInputObject) => {
	//construct filter based on user search params
	const filter = queryMakers.minesByLatLngMaterialRadius(userInputObject)

	//NOTE: business logic here (what to show)
	//alternative syntax collection.find({}).project({a:1})
	const targetFieldsObject = queryMakers.projectionMaker([
		'_id',
		'primary_canvass',
		'site_name',
		'primary_sic',
		'secondary_sic',
		'controller',
		'operator',
		'driving_directions',
		'nearest_town_or_city',
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

const findLandfillsByLatLngRadius = async (userInputObject) => {
	//construct filter based on user search params
	const filter = queryMakers.landfillsByLatLngRadius(userInputObject)

	//NOTE: business logic here (what to show)
	//alternative syntax collection.find({}).project({a:1})
	const targetFieldsObject = queryMakers.projectionMaker([
		'_id',
		'site_name',
		'controller',
		'operator',
		'driving_directions',
		'nearest_town_or_city',
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
	findById,
	findAllMaterials,
	findMinesByMaterialLatLngRadius,
	findLandfillsByLatLngRadius,
}
