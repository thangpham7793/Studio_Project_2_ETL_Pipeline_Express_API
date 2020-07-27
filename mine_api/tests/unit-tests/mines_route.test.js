const assert = require("assert");
const parsePath = require("./testUtils");
const longitude = "/@:lng(-\\d+)";
const materialParam = "/:material([a-zA-Z-_+]{1,})";

//following Google
const fullPath = "/:material([a-zA-Z-_+]{1,})/@:lng(-\\d+),:lat(\\d+)";

describe("Unit Test: Mines Route Path Regex", function () {
  describe(`the regex half path "/@:lng(-\\d+)"`, function () {
    it("should return null when the path begins with a non-digit character", function () {
      let path = "@/a123";
      let res = parsePath(longitude, path);
      assert.equal(null, res);
    });

    it("should return null when there's positive number", function () {
      let path = "/@123";
      let res = parsePath(longitude, path);
      assert.equal(null, res);
    });

    it("should return null when a backslash is missing", function () {
      let path = "@-123";
      let res = parsePath(longitude, path);
      assert.equal(null, res);
    });

    it("should return a negative number when the path contains a negative number", function () {
      let path = "/@-123";
      let res = parsePath(longitude, path);
      // console.log(res);
      assert.equal(true, res.includes(path));
    });

    it("should return null when the path contains a character despite the valid number", function () {
      let paths = ["/@a-123", "/@-1bdc23", "a/@-123", "/@-123bc"];
      paths.forEach((path) => {
        assert.equal(null, parsePath(longitude, path));
      });
    });
  });

  describe(`the regex for material ${materialParam}`, function () {
    it("should return only characters from the result regardless of case and delimiter", function () {
      let materials = [
        "/sand",
        "/Sand",
        "/SAND-and-Gravel",
        "/sand-and_Gravel",
        "/sandAndGravel",
        "/Dimension-Stone",
        "/Dimension+Stone",
      ];
      materials.forEach((material) => {
        let res = parsePath(materialParam, material);
        console.log("The result is " + res + "\n");
        assert.equal(true, res.includes(material));
      });
    });

    it("should return null if there's non-alphabetic input", function () {
      let materials = [
        "/material=sand123",
        "/material=123sand",
        "/material=sa23nd",
        "/material=12sand34",
        "/material=12sand%=?",
      ];
      materials.forEach((material) => {
        let res = parsePath(materialParam, material);
        console.log("The result is " + res + "\n");
        assert.equal(null, res);
      });
    });
  });

  describe(`the regex for the full path${fullPath}`, function () {
    it("should return correct urls regardless of case and delimiter", function () {
      let paths = [
        "/sand/@-123,30",
        "/sandAndGravel/@-123,30",
        "/Dimension-Stone/@-123,30",
        "/DimensionStone/@-123,30",
        "/Dimension_Stone/@-123,30",
        "/Dimension+Stone/@-123,30",
      ];
      paths.forEach((path) => {
        let res = parsePath(fullPath, path);
        assert.equal(true, res.includes(path));
      });
    });
  });
});

//TODO: rewrite the tests + regex after the group meeting tomorrow
//https://developers.google.com/web/updates/2016/01/urlsearchparams
//partial match or exact match?
//https://jordankasper.com/a-reintroduction-to-express.js-routes/
