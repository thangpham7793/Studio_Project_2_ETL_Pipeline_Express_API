<?php
  /*
   * File for an AJAX call that updates the requests table in the database
   */
  require '../../includes/dbh.inc.php';

  $requestID = $_POST['requestID'];
  $whatToUpdate = $_POST['update'];
  $requestSQL = "";

  // Update the relevant booleans
  if($whatToUpdate == "new") {
    $requestSQL = "UPDATE request SET pending = 0, completed = 0 WHERE requestID = ".$requestID;
  }
  else if($whatToUpdate == "pending") {
    $requestSQL = "UPDATE request SET pending = 1, completed = 0 WHERE requestID = ".$requestID;
  }
  else if($whatToUpdate == "completed") {
    $requestSQL = "UPDATE request SET pending = 0, completed = 1 WHERE requestID = ".$requestID;
  }

  // Echo out result - for testing, won't show on final AJAX call
  if(mysqli_query($conn, $requestSQL)) {
    echo "Record updated";
  }
  else {
    echo "Error updating record";
  }

  mysqli_close($conn);
?>
