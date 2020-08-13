const MongoClient = require('mongodb').MongoClient
const { MONGODB_APP_URI, CLIENT_CONFIG, LOCAL_URI } = require('../utils/config')
const client = new MongoClient(MONGODB_APP_URI, CLIENT_CONFIG)

module.exports = client
