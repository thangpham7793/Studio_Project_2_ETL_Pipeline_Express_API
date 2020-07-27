const assert = require("assert");
const routeRegex = require("../../utils/routeRegex");
const mockGetRequest = require("supertest");
const app = require("express")();
const mockGETRequestURL = "/Dimension+Stone/@-89,30";

const expectedParams = {
  material: "Dimension+Stone",
  lng: "-89",
  lat: "30",
};

app.get(routeRegex.minesByMaterialAndLatLng, function (req, res) {
  res.status(200).json(req.params);
});

describe.only("Unit Test: Search Mines Params Parser", function () {
  describe("GET /:material/@lng,lat", function () {
    it("should parse an object with the correct parameters from the mock request URL", function () {
      mockGetRequest(app)
        .get(mockGETRequestURL)
        .set("Accept", "application/json")
        .expect("Content-Type", /json/)
        .expect(200)
        .then((response) => {
          assert(response.body, expectedParams);
        });
    });
  });
});
