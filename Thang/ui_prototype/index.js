//ANCHOR: materialize stuff
M.AutoInit();

//ANCHOR: update slider-label
let sliderLabel = document.getElementsByClassName("slider-label")[0];
let sliderInput = document.getElementsByClassName("slider-input")[0];
sliderLabel.textContent = `Within ${sliderInput.value} Miles`;
sliderInput.oninput = function () {
  sliderLabel.textContent = `Within ${this.value} Miles`;
};

// ANCHOR: leaflet

const ACCESS_TOKEN =
  "pk.eyJ1IjoidGhhbmdwaGFtNzc5MyIsImEiOiJja2Jwb3VjangyYmE2MnJwZnhhbHR0aGUyIn0.nX_zeCSrkktjc3k148oQCA";

var mymap = L.map("mapid").setView([31, -100], 7);

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
).addTo(mymap);
