const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const middleware = require("./utils/middleware");

const minesRouter = require("./controllers/minesRouter");

//get methods from bodyParser
const { urlencoded, json } = bodyParser;

//parse incoming request using bodyParser
app.use(json());
app.use(urlencoded({ extended: false }));

app.get("/", (request, response) =>
  response.status(200).send({ message: "Welcome to the US Mines API Service" })
);

app.use("/mines", minesRouter);

//handle errors
app.use(middleware.unknownEndpoint);

module.exports = app;
