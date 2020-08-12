const http = require('http')
const logger = require('../utils/logger')
const client = require('./client.js')

const connectToDBAndStartServer = () => {
	client.connect(function (err) {
		if (err) {
			console.log('Failed to connect to Mongodb Atlas: ', err.message)
			return
		} else {
			console.log('Successfully connect to Mongodb Atlas')
			//only initialize express app when connected to database
			const app = require('../app')
			const server = http.createServer(app)
			const PORT = process.env.PORT || 3000

			//start server
			server.listen(PORT, () => {
				logger.info(`Listening on port ${PORT}`)
			})
			return app
		}
	})
}

module.exports = connectToDBAndStartServer
