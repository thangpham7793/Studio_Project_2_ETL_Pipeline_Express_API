$(document).ready(function() {
  var mymap = L.map('mapid').setView([51.505, -0.09], 13);
  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'your.mapbox.access.token'
}).addTo(mymap);

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
      pwdConfirm: pwdConfirm,
      signup-submit: "yes"
    });
  });
});
