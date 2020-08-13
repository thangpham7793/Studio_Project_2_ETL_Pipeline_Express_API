var map;
var allMaterials = {};
var searchRadiusCircle;
var markers = new Array();
var searchResults = new Array();
var materialsAtLocation = new Array();
var activeInfoWindow;
var selectedSupplier;

/* Handler for range slider
 * Updates the search radius shown to user on map and updates the shown data
 * based on current search criteria */
function updateRangeValue(val) {
  $("#searchRadiusDisplay").html(val);
  var address = $("#inputAddress").val();

  if(address != "") {
    var addressCoords = address.split(',');
    updateSearchCircle(addressCoords);
    updateSearchData(addressCoords, val);
    displayAvailableMaterials();
  }
}

/* Called by materialInput keyup
 * Updates what data is shown based on current search criteria */
function updateSearch() {
  var address = $("#inputAddress").val();
  var searchRadius = $("#sliderSearchRadius").val();

  if(address != "") {
    var addressCoords = address.split(',');
    updateSearchData(addressCoords, searchRadius);
  }
}

/* Retrieve list of all materials and add it to datalist. Makes it searchable
 * with dropdown from input box */
function getMaterials() {
  $.ajax({
    type: 'GET',
    url: 'https://us-mines-api.herokuapp.com/mines/materials',
    success: function (data) {
      allMaterials = data['materials'];
      displayAllMaterials();
    }
  });
}

function displayAllMaterials() {
  // Loop over all materials
  allMaterials.forEach((item, i) => {
    // Setup datalist option
    var option = document.createElement('option');
    option.setAttribute('value', item);

    // Add to datalist
    document.getElementById('materialList').appendChild(option);
  });
}

/* Removes all material from material search input and puts in only materials
 * that exist within the search radius and location */
function displayAvailableMaterials() {
  $("#materialList").empty();

  // Keep a list of all materials until a search has been done
  if(searchResults.length == 0) {
    displayAllMaterials();
  }
  else {
    materialsAtLocation.forEach((item, i) => {
      // Setup datalist option
      var option = document.createElement('option');
      option.setAttribute('value', item);

      // Add to datalist
      document.getElementById('materialList').appendChild(option);
    });
  }
}

// Enables the search button again
function enableSearch() {
  // Enable button again
  $("#btnSearch").prop('disabled', false);
  $("#btnSearch").text("Search");
}

/* AJAX call to API to query for suppliers using lat/lng and gets everything
 * in a 200 mile radius. Stores results in global variable "searchResults".
 * Processes all results to current search criteria to have them displayed to user. */
function searchForSupplier() {
  var address = $("#inputAddress").val();
  var addressCoords = address.split(',');

  // Check that inputs aren't empty
  if(address != "") {
    // Disable button until new search location is selected
    $("#btnSearch").prop('disabled', true);
    $("#btnSearch").text("Select a new location to enable a new search");

    // Inputs are correct, remove any highlights
    $("#inputAddress").removeClass("input-error");

    // Remove old search results
    $(".searchResult").remove();
    removeMarkers();
    materialsAtLocation = new Array();
    updateSearchCircle(addressCoords);

    // Add spinner to show user that something has happened after clicking search button
    $(".sidebar").append('<div id="loadingSpinner" class="spinner-border text-primary" role="status"> <span class="sr-only">Loading...</span> </div>');

    // 0 holds lat, 1 holds lng
    var addressCoords = address.split(',');

    // AJAX call to API to get list of suppliers
    $.ajax({
      type: 'GET',                                   //API uses lng/lat instead of lat/lng
      url: 'http://us-mines-api.herokuapp.com/mines/@' + addressCoords[1] + "," + addressCoords[0],
      statusCode: {
        // 400 means no result from the query
        400: function() {
          $("#loadingSpinner").remove();
          alert( "No result" );
        }
      },
      success: function (data) {
        // Remove spinner to show search has finished
        $("#loadingSpinner").remove();
        searchResults = data;

        // Loop over data(supplier info)
        data.forEach((item, i) => {
          if(itemMeetsSearchCriteria(item)) {
            if(!materialsAtLocation.includes(item['primary_sic'])) {
              materialsAtLocation.push(item['primary_sic']);
            }
            if(item['secondary_sic'] != undefined) {
              if(!materialsAtLocation.includes(item['secondary_sic'])) {
                materialsAtLocation.push(item['secondary_sic']);
              }
            }
            displayValidSearchResult(item);
          }
        });
        displayAvailableMaterials();
      }
    });
  }
  else { // Address input is empty, highlight to user
    if(address == "") {
      $("#inputAddress").addClass("input-error");
    }
  }
}

// Removes all markers from the map
function removeMarkers() {
  // Loop over markers and remove them from map
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  // Clear marker list
  markers = new Array();
}

// Remove existing search radius circle from map and create a new up to date one
function updateSearchCircle(addressCoords) {
  var searchRadius = $("#sliderSearchRadius").val();

  // Remove search radius from map
  if(searchRadiusCircle != undefined) {
    searchRadiusCircle.setMap(null);
  }

  // Add circle to the map to show search radius

  // 1609.34 meters to a mile
  var convertedMilesToMeters = searchRadius * 1609.34;

  var latLngObject = new google.maps.LatLng(addressCoords[0], addressCoords[1])
  // Add the circle for this city to the map.
  searchRadiusCircle = new google.maps.Circle({
    strokeColor: "#fcfc03",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#fcfc03",
    fillOpacity: 0.15,
    map,
    center: latLngObject,
    radius: convertedMilesToMeters
  });
}

/*
 * Returns the distance between 2 points in miles, uses the Haversine formula
 * found here: https://cloud.google.com/blog/products/maps-platform/how-calculate-distances-map-maps-javascript-api
*/
function getDistance(p1, p2) {
  var R = 3958.8; // Radius of the Earth in miles
  var rlat1 = p1[0] * (Math.PI/180); // Convert degrees to radians
  var rlat2 = p2[0] * (Math.PI/180); // Convert degrees to radians
  var difflat = rlat2-rlat1; // Radian difference (latitudes)
  var difflon = (p2[1]-p1[1]) * (Math.PI/180); // Radian difference (longitudes)

  var distanceMiles = 2 * R * Math.asin(Math.sqrt(Math.sin(difflat/2)*Math.sin(difflat/2)+Math.cos(rlat1)*Math.cos(rlat2)*Math.sin(difflon/2)*Math.sin(difflon/2)));
  return distanceMiles;
}

/* Loops over all stored search results and checks them against current
 * search criteria and displays it to the user */
function updateSearchData(address, searchRadius) {
  // Remove old search results
  $(".searchResult").remove();
  materialsAtLocation = new Array();
  removeMarkers();

  var material = $("#inputMaterial").val();

  // Loop over all search results
  searchResults.forEach((item, i) => {
    // If they meet the search criteria display the item to the user
    if(itemMeetsSearchCriteria(item)) {
      if(!materialsAtLocation.includes(item['primary_sic'])) {
        materialsAtLocation.push(item['primary_sic']);
      }
      if(item['secondary_sic'] != undefined) {
        if(!materialsAtLocation.includes(item['secondary_sic'])) {
          materialsAtLocation.push(item['secondary_sic']);
        }
      }

      displayValidSearchResult(item);
    }
  });
  displayAvailableMaterials();
}


/* Checks the item given through parameter against the search criteria and returns
 * true if it meets all of the search criteria (material, address set,
 *distance from address => search radius), else return false */
function itemMeetsSearchCriteria(item) {
  var address = $("#inputAddress").val();
  var material = $("#inputMaterial").val();
  var searchRadius = $("#sliderSearchRadius").val();

  // Doesn't meet criteria as no location to search by
  if(address != "") {
    // Input box for address currently sets "lat,lng", split to get individual values
    var addressCoords = address.split(',');

    // Get distance from address to the supplier           supplier coordinates come back as [lng,lat] needs to be reversed
    var distanceBetween = getDistance(addressCoords,[item['location']['coordinates'][1],item['location']['coordinates'][0]]);

    // If material entered use that as part of search criteria
    if(material != "") {
      var matchPrimary = false;
      var matchSecondary = false;

      // Check if SICs exist, check if entered material matches
      if(item['primary_sic'] != undefined) {
        if(item['primary_sic'].toLowerCase().includes(material.toLowerCase())) {
          matchPrimary = true;
        }
      }
      if(item['secondary_sic'] != undefined) {
        if(item['secondary_sic'].toLowerCase().includes(material.toLowerCase())) {
          matchSecondary = true;
        }
      }

      // If search material matches SIC then check by radius
      if(matchPrimary || matchSecondary) {
        // If distance is smaller than search area then matches all search criteria
        if(distanceBetween <= searchRadius) {
          return true;
        }
        else { // Not within search radius, doesn't meet criteria
          return false;
        }
      }
      else { // Doesn't have material search terms, doesn't meet criteria
        return false;
      }
    } // No material given to search by, just search by radius
    else { // No searc
      // If distance is smaller than search area then matches all search criteria
      if(distanceBetween <= searchRadius) {
        return true;
      }
      else { // Not within search radius, doesn't meet criteria
        return false;
      }
    }
  }
  else { // No address given, just return false
    return false;
  }
}

/* Takes supplier information as parameter, creates a div in sidebar with supplier
 * information displayed in it, creates onClick event for div to zoom in on supplier location.
 * Creates a marker at supplier location with popup of information about supplier
*/
function displayValidSearchResult(item) {
  // Create a div with class searchResult to display individual search results in
  var searchResultBox = $("<div></div>").addClass("searchResult");

  if(item['secondary_sic'] != undefined) {
    // Text that goes inside div
    var searchText = $("<p></p>").html("Supplier: " + item['site_name'] + "<br>Operator name: " +
    item['operator'] + "<br>Material: " + item['primary_sic'] + " & " + item['secondary_sic']);
  }
  else {
    // Text that goes inside div
    var searchText = $("<p></p>").html("Supplier: " + item['site_name'] + "<br>Operator name: " +
    item['operator'] + "<br>Material: " + item['primary_sic']);
  }


  // Add text to div
  searchResultBox.append(searchText);

  // Add div to sidebar
  $(".sidebar").append(searchResultBox);

  // HTML to add button to marker popup menu
  var requestPriceHTML = `
    <br>
    <div id="requestPriceContainer">
      <button type="button" class="btn btn-primary mb-2 btnRequestPrice"  data-toggle="modal" data-target="#modal_request_price" value=` + item['_id'] + `>Request Price For Delivery</button>
    </div>
  `;

  // Add marker to map
  // coord ends up being 0-lng, 1-lat
  var coord = item['location']['coordinates'];
  var latlngObject = new google.maps.LatLng(coord[1], coord[0])
  const marker = new google.maps.Marker({
    position: latlngObject,
    map: map
  });
  markers.push(marker);

  var infowindow;
  // Set marker popup menu
  if(item['secondary_sic'] != undefined) {
    infowindow = new google.maps.InfoWindow({
      content: "<b>Supplier:</b> " + item['site_name'] + "<br><b>Operator:</b> " + item['operator'] + "<br><b>Material:</b> " + item['primary_sic'] + " & " + item['secondary_sic'] + requestPriceHTML
    });
  }
  else {
    infowindow = new google.maps.InfoWindow({
      content: "<b>Supplier:</b> " + item['site_name'] + "<br><b>Operator:</b> " + item['operator'] + "<br><b>Material:</b> " + item['primary_sic'] + requestPriceHTML
    });
  }


  marker.addListener("click", () => {
    if(activeInfoWindow != undefined) {
      activeInfoWindow.close();
    }
    activeInfoWindow = infowindow;
    selectedSupplier = item;

    infowindow.open(map, marker);
  });

  //Add marker to array so it can be deleted later
  markers.push(marker);

  // Add onClick function to search result in side bar to zoom in on correlated marker
  searchResultBox.click(function() {
    if(activeInfoWindow != undefined) {
      activeInfoWindow.close();
    }
    activeInfoWindow = infowindow;
    selectedSupplier = item;

    map.setZoom(15);
    map.panTo(marker.getPosition());
    infowindow.open(map, marker);
  })
}

function init() {
  // Set up map
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40, lng: -100 },
    zoom: 4.5,
    mapTypeId: google.maps.MapTypeId.HYBRID,
    disableDefaultUI: true,
    zoomControl: true
  });

  // Retrieve material list on load
  getMaterials();

  // Map onclick event, get clicked lat/lng and put it in address input box, update any currently searched items
  map.addListener('click', function(mapsMouseEvent) {
    // Reset button to work again
    enableSearch();

    var lat = mapsMouseEvent.latLng.lat();
    var lng = mapsMouseEvent.latLng.lng() ;

    $("#inputAddress").val(lat + "," + lng);
    updateSearchCircle([lat, lng]);
    updateSearch();
  });

  // On modal close - empty feedback from request form
  $('#modal_request_price').on('hidden.bs.modal', function () {
    $("#submitRequest-feedback").empty();
  });
}

// Initialise everything that's needed on page load
window.onload = init;

// Prevent PHP submitting and reloading the page on form submissions
$(document).ready(function() {
  // Signup form submission
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

  // Request form submission
  $("#formRequestPrice").submit(function(event) {
    // Stop form submission
    event.preventDefault();

    // Extract all values from form
    var firstName = $("#inputRequestFirstName").val();
    var surname = $("#inputRequestSurname").val();
    var phone = $("#inputRequestPhone").val();
    var email = $("#inputRequestEmail").val();
    var address = $("#inputRequestAddress").val();
    var materials = $("#inputRequestMaterials").val();
    var addDetails = $("#inputRequestAddDetails").val();
    var coordinates = selectedSupplier['location']['coordinates'][0] + "," + selectedSupplier['location']['coordinates'][1];
    // TODO SET POST signup-submit
    // Run signup php code, pass through values. PHP echos out feedback
    // of submission into #submit-feedback element
    $("#submitRequest-feedback").load("includes/request_submit.inc.php", {
      firstName: firstName,
      surname: surname,
      phone: phone,
      email: email,
      address: address,
      materials: materials,
      addDetails: addDetails,
      supplierID: selectedSupplier['_id'],
      supplierMineName: selectedSupplier['site_name'],
      supplierControllerName: selectedSupplier['controller'],
      supplierOperatorName: selectedSupplier['operator'],
      supplierNearestTown: selectedSupplier['nearest_town_or_city'],
      supplierCoordinates: coordinates,
    });
  });
});
