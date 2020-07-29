var allMaterials = {};

$(document).ready(function() {
  $("form").submit(function(event) {
    event.preventDefault();
    var firstName = $("#inputFirstName").val();
    var surname = $("#inputSurname").val();
    var email = $("#inputEmail").val();
    var pwd = $("#inputPwd").val();
    var pwdConfirm = $("#inputPwdConfirm").val();

    // SET POST signup-submit
    $("#submit-feedback").load("includes/signup.inc.php", {
      firstName: firstName,
      surname: surname,
      email: email,
      pwd: pwd,
      pwdConfirm: pwdConfirm
    });
  });
});

function updateRangeValue(val) {
  $("#searchRadiusDisplay").html(val);
}

function getMaterials() {
  $.ajax({
    type: 'GET',
    url: 'https://us-mines-api.herokuapp.com/mines/materials',
    success: function (data) {
      allMaterials = data['materials'];
    }
  });
}

function searchMaterial(input) {
  var numMats = allMaterials.length;
  var inputLength = input.length;

  $("#materialList").html = "";

  for (var i = 0; i < numMats; i++) {
    if(((allMaterials[i].toLowerCase()).indexOf(input.toLowerCase())) > -1) {
      var node = document.createElement("option");
      var val = document.createTextNode(allMaterials[i]);
      node.appendChild(val);

      document.getElementById("materialList").appendChild(node);
    }
  }
}

function init() {
  getMaterials();
}

window.onload = init;


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

// https://nominatim.org/release-docs/develop/api/Search/ (to restrict search to USA)
// https://nominatim.org/release-docs/develop/develop/Import/
// must use https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 this America = US / can further restrict the search range for faster query time depending on other input
