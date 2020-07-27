const minesRouter = require("express").Router();
const routeHandlers = require("../server/routeHandlers");
const routeRegex = require("../utils/routeRegex");

require("express-async-errors");
//  (what client sends to me)
//get all (and this is where the client comes in, not me haha)
//basically don't expose things that can change
//TODO: how to add limit to requests?
minesRouter.get(
  routeRegex.minesByMaterialAndLatLng,
  async (request, response) => {
    let lng = parseFloat(request.params.lng),
      lat = parseFloat(request.params.lat),
      material = request.params.material;
    //radius = parseInt(request.params.radius);
    //TODO: this is where the error function comes in
    //TODO: should this be validated on the client side?
    if (lng < -180 || lng > 180 || lat < -90 || lat > 90) {
      response.status(400).send({
        message: "Invalid latitude or longitude!",
      });
      // } else if (radius <= 0) {
      //   response.status(400).send({ message: "Radius must be bigger than 0" });
    } else {
      let params = {
        lat,
        lng,
        material,
        //radius,
      };
      const result = await routeHandlers.findNearByMinesWithinRadius(params);
      //yay it works! So the question is should you close the connection there and then? And should you make a class?
      console.log(result);
      response.status(200).send(result);
    }
  }
);

//the format is router.{http_verb}
minesRouter.get("/", (request, response) => {
  response.status(200).send({
    message: "<h1>Welcome to the US Mines API Portal</h1>",
  });
});

//Lat-long coorditates for cities in United States are in range: Latitude from 19.50139 to 64.85694 and longitude from -161.75583 to -68.01197. (so longitude must be negative)
//? denotes optional expression, so that's probably why some of the routes has them

module.exports = minesRouter;

//TODO: incorporate radius into search URl
