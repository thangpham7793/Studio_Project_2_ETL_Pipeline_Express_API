const http = require("http");
const logger = require("./utils/logger");
const { PORT } = require("./utils/config");
const client = require("./server/client.js");

//keeping one connection open and reuse it throughout!
//https://stackoverflow.com/questions/14495975/why-is-it-recommended-not-to-close-a-mongodb-connection-anywhere-in-node-js-code
client.connect(function (err) {
  if (err) {
    console.log("Failed to connect to Mongodb Atlas: ", err.message);
    return;
  } else {
    console.log("Successfully connect to Mongodb Atlas");
    //only initialize express app when connected to database
    const app = require("./app");
    const server = http.createServer(app);

    server.listen(PORT, () => {
      logger.info(`Listening on port ${PORT}`);
    });
  }
});
