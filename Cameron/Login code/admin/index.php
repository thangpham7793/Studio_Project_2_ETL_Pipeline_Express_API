<?php
  require '../includes/dbh.inc.php';
?>

<!doctype html>
<html lang="en">
  <head>
      <!-- Required meta tags -->
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

      <!-- Bootstrap CSS -->
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
      <link rel="stylesheet" type="text/css" href="style.css">
      <title>Request admin</title>
  </head>
  <body>
    <!-- Main container that centers content -->
    <div id="centerContainer">
      <!-- Tab links -->
      <div class="btn-group btn-group-toggle" data-toggle="buttons">
        <label id="newButton" class="btn btn-secondary active">
          <input  type="radio" name="options"  onclick="tabChange(event, 'new')" checked> New
        </label>
        <label id="pendingButton" class="btn btn-secondary">
          <input type="radio" name="options" onclick="tabChange(event, 'pending')"> Pending
        </label>
        <label id="completedButton" class="btn btn-secondary">
          <input type="radio" name="options" onclick="tabChange(event, 'complete')"> Complete
        </label>
      </div>

      <!-- Tab content -->
      <div id="new" class="tabcontent">
        <?php
          // Get all new requests that haven't been looked at yet - order by descsending so most recent shows first
          $requestSQL = "SELECT * FROM request WHERE pending = 0 AND completed = 0  ORDER BY requestID DESC";
          $stmt = mysqli_stmt_init($conn);

          // Send prepared statement to server
          if (!mysqli_stmt_prepare($stmt, $requestSQL)) {
            echo "SQL error";
            exit();
          }
          else {

            // Run statement
            mysqli_stmt_execute($stmt);
            $requestResult = mysqli_stmt_get_result($stmt);

            // Loop over results and display to user
            while ($requestRow = mysqli_fetch_assoc($requestResult)) {
              echo '
              <div class="request">
                <h3>Customer Info:</h3>
                <p>
                  <b>Customer name:</b> '.$requestRow['userFirstName'].' '.$requestRow['userSurname'].'
                  <br />
                  <b>Customer phone:</b> '.$requestRow['userPhone'].'
                  <br />
                  <b>Customer email:</b> '.$requestRow['userEmail'].'
                  <br />
                  <b>Delivery address:</b> '.$requestRow['deliveryAddress'].'
                  <br />
                  <b>Requested materials:</b> '.$requestRow['materials'].'
                  <br />
                  <b>Additional details:</b> '.$requestRow['addDetails'].'
                </p>
                <h3>Supplier Info:</h3>
                <p>
                  <b>Mine name:</b> '.$requestRow['supplierMineName'].'
                  <br />
                  <b>Controller name:</b> '.$requestRow['supplierControllerName'].'
                  <br />
                  <b>Operator name:</b> '.$requestRow['supplierOperatorName'].'
                  <br />
                  <b>Nearest town:</b> '.$requestRow['supplierNearestTown'].'
                  <br />
                  <b>Lat/Lng coordinates:</b> '.$requestRow['supplierCoordinates'].'
                </p>
                <div class="buttons">
                  <button type="button" class="btn btn-primary update-button" onclick="moveToPending('.$requestRow['requestID'].')">Move to pending</button>
                  <button type="button" class="btn btn-primary update-button" onclick="moveToComplete('.$requestRow['requestID'].')">Move to complete</button>
                </div>
              </div>
              ';
            }
          }
         ?>
      </div>

      <div id="pending" class="tabcontent">
        <?php
          // Get all pending requests order by descending so most recent appears at top
          $requestSQL = "SELECT * FROM request WHERE pending = 1  ORDER BY requestID DESC";
          $stmt = mysqli_stmt_init($conn);

          // Send prepared statement to server
          if (!mysqli_stmt_prepare($stmt, $requestSQL)) {
            echo "SQL error";
            exit();
          }
          else {

            // Run statement
            mysqli_stmt_execute($stmt);
            $requestResult = mysqli_stmt_get_result($stmt);

            // Loop over results and display to user
            while ($requestRow = mysqli_fetch_assoc($requestResult)) {
              echo '
              <div class="request">
                <h3>Customer Info:</h3>
                <p>
                  <b>Customer name:</b> '.$requestRow['userFirstName'].' '.$requestRow['userSurname'].'
                  <br />
                  <b>Customer phone:</b> '.$requestRow['userPhone'].'
                  <br />
                  <b>Customer email:</b> '.$requestRow['userEmail'].'
                  <br />
                  <b>Delivery address:</b> '.$requestRow['deliveryAddress'].'
                  <br />
                  <b>Requested materials:</b> '.$requestRow['materials'].'
                  <br />
                  <b>Additional details:</b> '.$requestRow['addDetails'].'
                </p>
                <h3>Supplier Info:</h3>
                <p>
                  <b>Mine name:</b> '.$requestRow['supplierMineName'].'
                  <br />
                  <b>Controller name:</b> '.$requestRow['supplierControllerName'].'
                  <br />
                  <b>Operator name:</b> '.$requestRow['supplierOperatorName'].'
                  <br />
                  <b>Nearest town:</b> '.$requestRow['supplierNearestTown'].'
                  <br />
                  <b>Lat/Lng coordinates:</b> '.$requestRow['supplierCoordinates'].'
                </p>
                <div class="buttons">
                  <button type="button" class="btn btn-primary update-button" onclick="moveToNew('.$requestRow['requestID'].')">Move to New</button>
                  <button type="button" class="btn btn-primary update-button" onclick="moveToComplete('.$requestRow['requestID'].')">Move to complete</button>
                </div>
              </div>
              ';
            }
          }
         ?>
      </div>

      <div id="complete" class="tabcontent">
        <?php
          // Select all completed requests - order by descending so most recent shows first
          $requestSQL = "SELECT * FROM request WHERE completed = 1  ORDER BY requestID DESC";
          $stmt = mysqli_stmt_init($conn);

          // Send prepared statement to server
          if (!mysqli_stmt_prepare($stmt, $requestSQL)) {
            echo "SQL error";
            exit();
          }
          else {

            // Run statement
            mysqli_stmt_execute($stmt);
            $requestResult = mysqli_stmt_get_result($stmt);

            // Loop over results and display to user
            while ($requestRow = mysqli_fetch_assoc($requestResult)) {
              echo '
              <div class="request">
                <h3>Customer Info:</h3>
                <p>
                  <b>Customer name:</b> '.$requestRow['userFirstName'].' '.$requestRow['userSurname'].'
                  <br />
                  <b>Customer phone:</b> '.$requestRow['userPhone'].'
                  <br />
                  <b>Customer email:</b> '.$requestRow['userEmail'].'
                  <br />
                  <b>Delivery address:</b> '.$requestRow['deliveryAddress'].'
                  <br />
                  <b>Requested materials:</b> '.$requestRow['materials'].'
                  <br />
                  <b>Additional details:</b> '.$requestRow['addDetails'].'
                </p>
                <h3>Supplier Info:</h3>
                <p>
                  <b>Mine name:</b> '.$requestRow['supplierMineName'].'
                  <br />
                  <b>Controller name:</b> '.$requestRow['supplierControllerName'].'
                  <br />
                  <b>Operator name:</b> '.$requestRow['supplierOperatorName'].'
                  <br />
                  <b>Nearest town:</b> '.$requestRow['supplierNearestTown'].'
                  <br />
                  <b>Lat/Lng coordinates:</b> '.$requestRow['supplierCoordinates'].'
                </p>
                <div class="buttons">
                  <button type="button" class="btn btn-primary update-button" onclick="moveToNew('.$requestRow['requestID'].')">Move to New</button>
                  <button type="button" class="btn btn-primary update-button" onclick="moveToPending('.$requestRow['requestID'].')">Move to Pending</button>
                </div>
              </div>
              ';
            }
          }
         ?>
      </div>

    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0="  crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
    <script type="text/javascript" src="script.js"></script>
  </body>
</html>
