const callbacks = require("../utils/callbacks");
const queryMaker = require("../utils/queryMaker");
const client = require("./client");

//global collection to share through each handler
const db = client.db("us-mines-locations");
const collection = db.collection("msha");

//can have a look up table depending on the method use as well
function getRequestHandlerFactory(
  queryHandler,
  queryOperation,
  resultProcessor
) {
  return async function (userInputObject) {
    const query = queryHandler(userInputObject);
    console.log(query);
    let result;
    try {
      result = await collection[queryOperation](query).limit(1).toArray();
      return resultProcessor(result);
    } catch (error) {
      console.error(error);
    }
  };
}

const findNearByMinesWithinRadius = getRequestHandlerFactory(
  queryMaker.findNearByMinesWithin,
  "find",
  callbacks.processNearbyMinesResults
);

module.exports = {
  findNearByMinesWithinRadius,
};
