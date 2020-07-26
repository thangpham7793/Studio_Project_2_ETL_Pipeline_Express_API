const minesRouter = require("express").Router();
const routeHandlers = require("../server/routeHandlers");

require("express-async-errors");
//  (what client sends to me)
//get all (and this is where the client comes in, not me haha)
//basically don't expose things that can change
minesRouter.get("/material/@:lng.:lat", async (request, response) => {
  let lng = parseFloat(request.params.lng),
    lat = parseFloat(request.params.lat),
    material = request.params.material;
  //TODO: this is where the error function comes in
  //TODO: should this be validated on the client side?
  if (lng < -180 || lng > 180 || lat < -90 || lat > 90) {
    response.status(400).send({
      message: "Invalid latitude or longitude!",
    });
  } else {
    let params = {
      lat,
      lng,
      material,
    };
    const result = await routeHandlers.findNearByMinesWithinRadius(params);
    //yay it works! So the question is should you close the connection there and then? And should you make a class (yes you really should?)
    console.log(result);
    response.status(200).send({
      result,
    });
  }
});

//the format is router.{http_verb}
minesRouter.get("/", (request, response) => {
  response.status(200).send({
    message: "<h1>Welcome to the US Mines API Portal</h1>",
  });
});

module.exports = minesRouter;
