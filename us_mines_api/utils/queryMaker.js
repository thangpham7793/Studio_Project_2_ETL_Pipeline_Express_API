const CIRCLE_CENTER = 5 / 3963.2
const METERS_PER_MILE = 1609.34

//In addition to supporting queries that match on all the index fields, compound indexes can support queries that match on the prefix of the index fields. That is, the index supports queries on the item field as well as both item and stock fields:

//https://docs.mongodb.com/v4.0/core/index-compound/#compound-index-prefix

//basically any queries that match one or more of the indexes except for the last one
//however, it must always starts with the first prefix (the first index!)
//so in our case the first index should be 2dsphere, followed by materials? (since Eric wants this)
//https://docs.mongodb.com/v4.0/core/index-multikey/ (this is important) (if we hardcode the values on the client side, then it ensures that => this also mean we need to clean up the materials during the ETL => so may be indexing on NAICS/SIC code?)
//location/geometry => materials

//sort order could be -1 because ppl may look up for sand + gravel the most

//okay I think I know why! It's because the loc is taken as a string rather than a nested document. Hmm, this means that it may not be possible to do it this way...Quicker if you put the coordinates first as well

//TODO: should use text index since the codes are limited and we can search for exact match! https://stackoverflow.com/questions/35812680/searching-in-mongo-db-using-mongoose-regex-vs-text
//https://stackoverflow.com/questions/50067786/mongo-text-search-with-regular-expression
//https://docs.mongodb.com/manual/core/index-text/#index-entries
//https://docs.mongodb.com/manual/core/index-text/#tokenization-delimiters
//text index in this case shouldn't be too hard, since there are only a couple of materials
//https://docs.atlas.mongodb.com/reference/atlas-search/tutorial/ can use Atlas Search
// https://docs.atlas.mongodb.com/reference/atlas-search/tutorial/
const findNearByMinesWithin = ({ lat, lng, material, radius }) => {
	console.log(
		`Finding ${material} mines around ${lat} latitude and ${lng} longitude within 50 miles`
	)
	return {
		primary_sic: { $regex: `${material}`, $options: 'gi' },
		location: {
			$near: {
				$geometry: {
					type: 'Point',
					coordinates: [lng, lat],
				},
				$maxDistance: radius * METERS_PER_MILE,
			},
		},
	}
}

const projectionMaker = (fieldsArr) => {
	projectionObject = fieldsArr.reduce(
		(projectionObject, field) => {
			return {
				...projectionObject,
				[field]: 1,
			}
		},
		{ _id: 0 }
	)
	return projectionObject
}

module.exports = {
	findNearByMinesWithin,
	projectionMaker,
}
