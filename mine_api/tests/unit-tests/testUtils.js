const { pathToRegexp } = require("path-to-regexp");

function parsePath(pattern, input) {
  const regexp = pathToRegexp(pattern);
  return regexp.exec(input);
}

module.exports = parsePath;
