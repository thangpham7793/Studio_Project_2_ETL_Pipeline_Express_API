require('dotenv').config()

/**
 * Load ENV variables from .env
 */

module.exports = {
	PORT: process.env.PORT || 3000,
	MONGODB_URI: process.env.MONGODB_APP_URI,
	MONGODB_NAME: process.env.MONGODB_NAME,
	MONGODB_COLLECTION: process.env.MONGODB_COLLECTION,
	CLIENT_CONFIG: { useNewUrlParser: true, useUnifiedTopology: true },
	LOCAL_URI: 'mongodb://localhost:27017',
	DB_NAME: 'test',
}
