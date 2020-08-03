const METERS_PER_MILE = 1609.34

const findNearByMinesWithin = ({ lat, lng, material }) => {
	console.log(
		`Finding ${material} mines around ${lat} latitude and ${lng} longitude within 50 miles`
	)
	//NOTE: MONGODB uses implicit AND. So the below query is:
	// Find all mines with material as primary or secondary AND near a particular point within a fixed radius
	return {
		$or: [
			{ primary_sic: { $regex: `${material}`, $options: 'gi' } },
			{ secondary_sic: { $regex: `${material}`, $options: 'gi' } },
		],
		location: {
			$near: {
				$geometry: {
					type: 'Point',
					coordinates: [lng, lat],
				},
				$maxDistance: 200 * METERS_PER_MILE,
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
