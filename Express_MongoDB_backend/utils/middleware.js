const logger = require("./logger");

//unknown endpoint err
const unknownEndpoint = (request, response) => {
  response.status(404).send({ error: "unknown endpoint" });
};

const errorHandler = (error, request, response, next) => {
  next(error);
};

module.exports = {
  unknownEndpoint,
  errorHandler,
};