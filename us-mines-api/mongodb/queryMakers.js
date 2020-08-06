const METERS_PER_MILE = 1609.34

/**
 * The below functions construct MongoDB Queries For Each Requests
 * from the search queries in the params.body
 * @param {params.body}
 *
 * For geo-related queries in MongoDB: https://docs.mongodb.com/manual/reference/operator/query/near/#op._S_near
 */

const minesByLatLngMaterialRadius = ({ lat, lng, material, radius }) => {
	const inputRadius = radius || 200
	if (material != undefined) {
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
	} else {
		return {
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

//find all mines regardless of materials
const allMinesByLatLng = ({ lat, lng, radius }) => {
	const inputRadius = radius || 200
	return {
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

module.exports = {
	allMinesByLatLng,
	minesByLatLngMaterialRadius,
	projectionMaker,
}
