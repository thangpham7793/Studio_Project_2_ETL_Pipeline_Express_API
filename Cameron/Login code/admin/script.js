function moveToNew(requestID) {
  if(typeof(Storage) !== "undefined") {
    if($("#newButton").hasClass("active")){
      //Store old state
      localStorage.setItem("state","new");
    }
    if($("#pendingButton").hasClass("active")){
      //Store old state
      localStorage.setItem("state","pending");
    }
    if($("#completedButton").hasClass("active")){
      //Store old state
      localStorage.setItem("state","completed");
    }
  }

  // AJAX to php to update the request in database
  $.post("includes/updateRequest.inc.php", {
    requestID: requestID,
    update: "new",
  });
  // Reload page to update the request to it's new tab
  location.reload();
}

function moveToPending(requestID) {
  if(typeof(Storage) !== "undefined") {
    if($("#newButton").hasClass("active")){
      //Store old state
      localStorage.setItem("state","new");
    }
    if($("#pendingButton").hasClass("active")){
      //Store old state
      localStorage.setItem("state","pending");
    }
    if($("#completedButton").hasClass("active")){
      //Store old state
      localStorage.setItem("state","completed");
    }
  }

  // AJAX to php to update the request in database
  $("#feedback").load("includes/updateRequest.inc.php", {
    requestID: requestID,
    update: "pending",
  });
  // Reload page to update the request to it's new tab
  location.reload();
}

function moveToComplete(requestID) {
  if(typeof(Storage) !== "undefined") {
    if($("#newButton").hasClass("active")){
      //Store old state
      localStorage.setItem("state","new");
    }
    if($("#pendingButton").hasClass("active")){
      //Store old state
      localStorage.setItem("state","pending");
    }
    if($("#completedButton").hasClass("active")){
      //Store old state
      localStorage.setItem("state","completed");
    }
  }

  // AJAX to php to update the request in database
  $("#feedback").load("includes/updateRequest.inc.php", {
    requestID: requestID,
    update: "completed",
  });
  // Reload page to update the request to it's new tab
  location.reload();
}

function tabChange(evt, requestType) {
  // Get all elements with class="tabcontent" and hide them
  var tabcontent = document.getElementsByClassName("tabcontent");
  for (var i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Set the div element to show
  document.getElementById(requestType).style.display = "block";
}

function init() {
  //Retrieve state
  var state = localStorage.getItem("state");

  // If state was new then show new requests
  if(state == "new" || state == null) {
    document.getElementById("new").style.display = "block";
    $("#pendingButton").removeClass("active");
    $("#completedButton").removeClass("active");
    $("#newButton").addClass("active");

  }
  // If state was pending show pending requests
  else if(state == "pending") {
    document.getElementById("pending").style.display = "block";
    $("#newButton").removeClass("active");
    $("#completedButton").removeClass("active");
    $("#pendingButton").addClass("active");

  }
  // If state was completed then show completed requests
  else if(state == "completed") {
    document.getElementById("complete").style.display = "block";
    $("#newButton").removeClass("active");
    $("#pendingButton").removeClass("active");
    $("#completedButton").addClass("active");

  }
}

window.onload = init;
