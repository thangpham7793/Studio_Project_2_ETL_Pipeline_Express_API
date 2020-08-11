<?php
  require 'includes/dbh.inc.php';

  // '?' is a standin that is replaced during binding
  $sql = "SELECT * FROM request";
  $stmt = mysqli_stmt_init($conn);

  // Send prepared statement to server
  if (!mysqli_stmt_prepare($stmt, $sql)) {
    echo "SQL error";
    exit();
  }
  else {

    // Run statement
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);

    // Get result as an associative(named keys) array
    while ($row = mysqli_fetch_assoc($result)) {
      echo $row['supplierName'];
      echo "<br>";
    }
  }
 ?>
