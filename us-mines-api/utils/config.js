require('dotenv').config()

const MONGODB_APP_URI = `mongodb+srv://${process.env.MONGODB_USERNAME}:${process.env.MONGODB_PASSWORD}@${process.env.MONGODB_CLUSTER}.leaav.mongodb.net/${process.env.MONGODB_NAME}?retryWrites=true&w=majority`

module.exports = {
	PORT: process.env.PORT || 3000,
	MONGODB_URI: MONGODB_APP_URI,
	CLIENT_CONFIG: { useNewUrlParser: true, useUnifiedTopology: true },
	LOCAL_URI: 'mongodb://localhost:27017',
	DB_NAME: 'test',
}
