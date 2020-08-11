<?php
// Check user got here from signup form
//if (isset($_POST['signup-submit'])) {
    // Start DB connection
    require 'dbh.inc.php';

    // Collect info from POST
    $firstName = $_POST['firstName'];
    $surname = $_POST['surname'];
    $phone = $_POST['phone'];
    $email = $_POST['email'];
    $address = $_POST['address'];
    $materials = $_POST['materials'];
    $addDetails = $_POST['addDetails'];
    $supplierID = $_POST['supplierID'];
    $supplierName = $_POST['supplierName'];

    $emptyFirstName = false;
    $emptySurname = false;
    $emptyPhone = false;
    $emptyEmail = false;
    $emptyAddress = false;
    $emptyMaterials = false;
    $invalidEmail = false;
    $validInputs = true;

    // Check if all fields have values
    if(empty($firstName)) {
      $emptyFirstName = true;
    }
    if(empty($surname)) {
      $emptySurname = true;
    }
    if(empty($phone)) {
      $emptyPhone = true;
    }
    if(empty($email)) {
      $emptyEmail = true;
    }
    if(empty($address)) {
      $emptyAddress = true;
    }
    if(empty($materials)) {
      $emptyMaterials = true;
    }

    // Inform user of empty fields
    if($emptyFirstName || $emptySurname || $emptyPhone || $emptyEmail || $emptyAddress || $emptyMaterials) {
      echo "<span class='form-error'>Fill in all fields</span>";
      $validInputs = false;
    }
    else {
      // Check if valid email, inform user if not
      if(!filter_var($email, FILTER_VALIDATE_EMAIL)) {
          $invalidEmail = true;
          $validInputs = false;
          echo "<span class='form-error'>Invalid email</span>";
      }
    }

    // Check if all inputs are valid, enter info into DB
    if($validInputs) {
      // Fresh user, prepare SQL. '?' is a standin that is replaced during binding
      $sql = "INSERT INTO request(userFirstName, userSurname, userPhone, userEmail, deliveryAddress, materials, addDetails, supplierID, supplierName) VALUES(?,?,?,?,?,?,?,?,?)";
      $stmt = mysqli_stmt_init($conn);

      //Send prepared statement to server
      if (!mysqli_stmt_prepare($stmt, $sql)) {
        header("Location: ../index.php?error=sqlerror");
        exit();
      }
      else {
        // Bind parameters to statement
        mysqli_stmt_bind_param($stmt, "sssssssss", $firstName, $surname, $phone, $email, $address, $materials, $addDetails, $supplierID, $supplierName);

        // Run statement
        mysqli_stmt_execute($stmt);
        echo "<span class='form-success'>Request submission successful!</span>";
        ?>
        <script>
            $("#inputRequestFirstName, #inputRequestSurname, #inputRequestPhone, #inputRequestEmail, #inputRequestAddress, #inputRequestMaterials").removeClass("input-error");
            $("#inputRequestFirstName").val("");
            $("#inputRequestSurname").val("");
            $("#inputRequestPhone").val("");
            $("#inputRequestEmail").val("");
            $("#inputRequestAddress").val("");
            $("#inputRequestMaterials").val("");
            $("#inputRequestAddDetails").val("");
        </script>
        <?php
      }
    }
    else { // Error in user input, apply styling to help user fill in correct inputs
      ?>
      <script>
        $("#inputRequestFirstName, #inputRequestSurname, #inputRequestPhone, #inputRequestEmail, #inputRequestAddress, #inputRequestMaterials").removeClass("input-error");

        var emptyFirstName = "<?php echo $emptyFirstName ?>";
        var emptySurname = "<?php echo $emptySurname ?>";
        var emptyPhone = "<?php echo $emptyPhone ?>";
        var emptyEmail = "<?php echo $emptyEmail ?>";
        var emptyAddress = "<?php echo $emptyAddress ?>";
        var emptyMaterials = "<?php echo $emptyMaterials ?>";
        var invalidEmail = "<?php echo $invalidEmail ?>";

        // Apply styling to invalid boxes
        if(emptyFirstName || emptySurname || emptyPhone || emptyEmail || emptyAddress || emptyMaterials || invalidEmail) {
            if(emptyFirstName) {
              $("#inputRequestFirstName").addClass("input-error");
            }
            if(emptySurname) {
              $("#inputRequestSurname").addClass("input-error");
            }
            if(emptyPhone) {
              $("#inputRequestPhone").addClass("input-error");
            }
            if(emptyEmail || invalidEmail) {
              $("#inputRequestEmail").addClass("input-error");
            }
            if(emptyAddress) {
              $("#inputRequestAddress").addClass("input-error");
            }
            if(emptyMaterials) {
              $("#inputRequestMaterials").addClass("input-error");
            }
        }
      </script>

      <?php
    }

    // Close connections
    if(isset($stmt)) {
      mysqli_stmt_close($stmt);
    }

    mysqli_close($conn);
//}
//else {
  // User did not get here through form, send them back
  //header("Location: ../index.php");
  //exit();
//}
?>
