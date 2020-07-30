// ANCHOR: leaflet

const ACCESS_TOKEN =
  "pk.eyJ1IjoidGhhbmdwaGFtNzc5MyIsImEiOiJja2Jwb3VjangyYmE2MnJwZnhhbHR0aGUyIn0.nX_zeCSrkktjc3k148oQCA";

const map = L.map("map").setView([31, -100], 7);

L.tileLayer(
  `https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${ACCESS_TOKEN}`,
  {
    attribution: `Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>`,
    maxZoom: 18,
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1,
    accessToken: ACCESS_TOKEN,
  }
).addTo(map);

function selectedResultDatabaseCall(result) {
  let addressArr = result.name.replace(" ", "").split(",");
  let { lat, lng } = result.center;
  console.log(addressArr, lat, lng);
}

// this is based on the source code of the plugin, and I'm just adding one line to get result from the api call and do sth with it
L.Control.Geocoder.prototype._geocodeResultSelected = function (result) {
  selectedResultDatabaseCall(result); //this is my code
  this.fire("markgeocode", { geocode: result });
};

geocoderConfig = {
  position: "topleft",
  collapsed: false,
  placeholder: "Street Address...",
  geocoder: L.Control.Geocoder.nominatim(nominatimConfig),
  iconLabel: "Enter Street Address",
};

L.Control.geocoder(geocoderConfig).addTo(map);

// https://nominatim.org/release-docs/develop/api/Search/ (to restrict search to USA)
// https://nominatim.org/release-docs/develop/develop/Import/
// must use https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 this America = US / can further restrict the search range for faster query time depending on other input
