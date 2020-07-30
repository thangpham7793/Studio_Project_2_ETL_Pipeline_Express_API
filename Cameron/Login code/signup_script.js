var allMaterials = {};

// Prevent PHP submitting and reloading the page on signup form submission
$(document).ready(function() {
  $("#formSignup").submit(function(event) {
    // Stop form submission
    event.preventDefault();

    // Extract all values from form
    var firstName = $("#inputFirstName").val();
    var surname = $("#inputSurname").val();
    var email = $("#inputEmail").val();
    var pwd = $("#inputPwd").val();
    var pwdConfirm = $("#inputPwdConfirm").val();

    // TODO SET POST signup-submit
    // Run signup php code, pass through values. PHP echos out feedback
    // of submission into #submit-feedback element
    $("#submit-feedback").load("includes/signup.inc.php", {
      firstName: firstName,
      surname: surname,
      email: email,
      pwd: pwd,
      pwdConfirm: pwdConfirm
    });
  });
});

// Handler for slider to update text field showing search radius
function updateRangeValue(val) {
  $("#searchRadiusDisplay").html(val);
}

// Retrieve list of all materials and add it to datalist. Makes it searchable
// with dropdown from input box
function getMaterials() {
  $.ajax({
    type: 'GET',
    url: 'https://us-mines-api.herokuapp.com/mines/materials',
    success: function (data) {
      allMaterials = data['materials'];

      // Loop over all materials
      allMaterials.forEach((item, i) => {
        // Setup datalist option
        var option = document.createElement('option');
        option.setAttribute('value', item);

        // Add to datalist
        document.getElementById('materialList').appendChild(option);
      });

    }
  });
}

/* AJAX call to API to query for suppliers of given material */
function searchForSupplier() {
  $( ".searchResult" ).remove();

  var address = $("#inputAddress").val();
  var material = $("#inputMaterial").val();
  var searchRadius = $("#sliderSearchRadius").val();

  material = material.split(' ').join('+');

  // Check that inputs aren't empty
  if(address != "" && material != "") {
    // AJAX call to API to get list of suppliers
    $.ajax({
      type: 'GET',                                //Material/@lng,lat,search radius(miles)
      url: 'http://us-mines-api.herokuapp.com/mines/' + material + '/@' + address + ',' + searchRadius,
      statusCode: {
        // 400 means no result from the query
        400: function() {
          // TODO handle no result search
          alert( "No result" );
        }
      },
      success: function (data) {
        // Loop over data(supplier info)
        data.forEach((item, i) => {
          // Create a div with class searchResult to display individual search results in
          var searchResultBox = $("<div></div>").addClass("searchResult");

          // Text that goes inside div
          var searchText = $("<p></p>").html("Supplier: " + item['current_mine_name'] + "<br>Operator name: " +
          item['current_operator_name'] + "<br>Location: " + item['location']['coordinates']);

          // Add text to div
          searchResultBox.append(searchText);

          //Add div to sidebar
          $(".sidebar").append(searchResultBox);
        });
      }
    });
  }
}


function init() {
  // Retrieve material list on load
  getMaterials();
}

// Initialise everything that's needed on page load
window.onload = init;


/*
  Leaflet code
*/
const ACCESS_TOKEN =
  "pk.eyJ1IjoidGhhbmdwaGFtNzc5MyIsImEiOiJja2Jwb3VjangyYmE2MnJwZnhhbHR0aGUyIn0.nX_zeCSrkktjc3k148oQCA";

const map = L.map("map").setView([40, -100], 5.4);

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
