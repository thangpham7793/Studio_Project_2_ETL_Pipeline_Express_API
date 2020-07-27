const callbacks = require("../utils/callbacks");
const queryMaker = require("../utils/queryMaker");
const client = require("./client");

//global collection to share through each handler
const db = client.db("us-mines-locations");
const collection = db.collection("msha");

//can have a look up table depending on the method use as well
function getRequestHandlerFactory(
  queryHandler,
  projectionMaker,
  queryOperation,
  resultProcessor
) {
  return async function (userInputObject) {
    const filter = queryHandler(userInputObject);
    //NOTE: business logic here (what to show)
    const projection = projectionMaker([
      "current_mine_name",
      "primary_sic",
      "primary_canvass",
    ]);
    console.log(filter, projection); //FIXME: how to add projection using Mongod Driver?
    let result;
    try {
      result = await collection[queryOperation](filter, projection)
        .limit(1)
        .toArray();
      return resultProcessor(result);
    } catch (error) {
      console.error(error);
    }
  };
}

const findNearByMinesWithinRadius = getRequestHandlerFactory(
  queryMaker.findNearByMinesWithin,
  queryMaker.projectionMaker,
  "find",
  callbacks.processNearbyMinesResults
);

module.exports = {
  findNearByMinesWithinRadius,
};
