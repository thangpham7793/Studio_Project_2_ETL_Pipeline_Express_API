const METERS_PER_MILE = 1609.34

const findNearByMinesWithin = ({ lat, lng, material, radius }) => {
	//NOTE: MONGODB uses implicit AND. So the below query is:
	// Find all mines with material as primary or secondary AND near a particular point within a fixed radius
	const inputRadius = radius || 200
	console.log('The radius is ' + inputRadius)
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
				$maxDistance: inputRadius * METERS_PER_MILE,
			},
		},
	}
}

//include and exclude fields in results (1 is include and 0 is exclude)
const projectionMaker = (fieldsArray) => {
	targetFieldsObject = fieldsArray.reduce((projectionObject, field) => {
		return {
			...projectionObject,
			[field]: 1,
		}
	}, {})

	return targetFieldsObject
}

module.exports = {
	findNearByMinesWithin,
	projectionMaker,
}
