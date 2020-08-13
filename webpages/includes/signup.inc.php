<?php
// Check user got here from signup form
if (isset($_POST['signupSubmit'])) {
    // Start DB connection
    require 'dbh.inc.php';

    // Collect info from POST
    $firstName = $_POST['firstName'];
    $surname = $_POST['surname'];
    $email = $_POST['email'];
    $password = $_POST['pwd'];
    $passwordConfirm = $_POST['pwdConfirm'];

    $emptyFirstName = false;
    $emptySurname = false;
    $emptyEmail = false;
    $emptyPwd = false;
    $emptyPwdConfirm = false;
    $emailTaken = false;
    $signupSuccess = false;
    $invalidEmail = false;
    $invalidPasswordMatch = false;

    // Check if all fields have values
    if(empty($firstName)) {
      $emptyFirstName = true;
    }
    if(empty($surname)) {
      $emptySurname = true;
    }
    if(empty($email)) {
      $emptyEmail = true;
    }
    if(empty($password)) {
      $emptyPwd = true;
    }
    if(empty($passwordConfirm)) {
      $emptyPwdConfirm = true;
    }

    // Inform user of empty fields
    if($emptyFirstName || $emptySurname || $emptyEmail || $emptyPwd || $emptyPwdConfirm) {
      echo "<span class='form-error'>Fill in all fields</span>";
    }
    else {
      // Check if valid email, inform user if not
      if(!filter_var($email, FILTER_VALIDATE_EMAIL)) {
          $invalidEmail = true;
          echo "<span class='form-error'>Invalid email</span>";
      }
      else {
        // Check if passwords match, inform user if they don't
        if($password !== $passwordConfirm) {
          echo "<span class='form-error'>Passwords do not match</span>";
          $invalidPasswordMatch = true;
        }
      }
    }

    // Check if all inputs are valid, enter info into DB
    if(!$emptyFirstName && !$emptySurname && !$emptyPwd && !$emptyPwdConfirm && !$invalidEmail && !$invalidPasswordMatch) {
        // '?' is a standin that is replaced during binding
        // Following code checks if email already exists in DB
        $sql = "SELECT email FROM user WHERE email=?";
        $stmt = mysqli_stmt_init($conn);

        // Send prepared statement to server
        if(!mysqli_stmt_prepare($stmt, $sql)) {
          echo "<span class='form-error'>SQL Error</span>";
          exit();
        }
        else {
          // Bind parameters to statement
          mysqli_stmt_bind_param($stmt, "s", $email);
          // Run statement
          mysqli_stmt_execute($stmt);
          mysqli_stmt_store_result($stmt);
          $resultCheck = mysqli_stmt_num_rows($stmt);

          // If there are results, email is already in DB
          if ($resultCheck > 0) {
            $emailTaken = true;
            echo "<span class='form-error'>Email taken</span>";
          }
          else {
            if(!$emailTaken) {
              // Fresh user, prepare SQL. '?' is a standin that is replaced during binding
              $sql = "INSERT INTO user(firstName, surname, email, password) VALUES(?,?,?,?)";
              $stmt = mysqli_stmt_init($conn);

              //Send prepared statement to server
              if (!mysqli_stmt_prepare($stmt, $sql)) {
                //header("Location: ../index.php?error=sqlerror");
                exit();
              }
              else {
                // Hash password with salt using bcrypt, default in PHP
                $hasedPwd = password_hash($password, PASSWORD_DEFAULT);

                // Bind parameters to statement
                mysqli_stmt_bind_param($stmt, "ssss", $firstName, $surname, $email, $hasedPwd);

                // Run statement
                mysqli_stmt_execute($stmt);
                $signupSuccess = true;
                echo "<span class='form-success'>Signup successful!</span>";
                ?>

                <script>
                  var signupSuccess = "<?php echo $signupSuccess ?>";

                  if(signupSuccess) {
                    $("#inputFirstName, #inputSurname, #inputEmail, #inputPwd, #inputPwdConfirm").removeClass("input-error");
                    $("#inputFirstName, #inputSurname, #inputEmail, #inputPwd, #inputPwdConfirm").addClass("input-success");
                    $("#inputFirstName").val("");
                    $("#inputSurname").val("");
                    $("#inputEmail").val("");
                    $("#inputPwd").val("");
                    $("#inputPwdConfirm").val("");
                  }
                </script>

                <?php
              }
            }
          }
        }
    }
    else { // Error in user input, apply styling to help user fill in correct inputs
      ?>
      <script>
        $("#inputFirstName, #inputSurname, #inputEmail, #inputPwd, #inputPwdConfirm").removeClass("input-error");

        var emptyFirstName = "<?php echo $emptyFirstName ?>";
        var emptySurname = "<?php echo $emptySurname ?>";
        var emptyEmail = "<?php echo $emptyEmail ?>";
        var emptyPwd = "<?php echo $emptyPwd ?>";
        var emptyPwdConfirm = "<?php echo $emptyPwdConfirm ?>";
        var emailTaken = "<?php echo $emailTaken ?>";
        var invalidEmail = "<?php echo $invalidEmail ?>";
        var invalidPasswordMatch = "<?php echo $invalidPasswordMatch ?>";

        // Apply styling to invalid boxes
        if(emptyFirstName || emptySurname || emptyEmail || emptyPwd || emptyPwdConfirm) {
            if(emptyFirstName) {
              $("#inputFirstName").addClass("input-error");
            }
            if(emptySurname) {
              $("#inputSurname").addClass("input-error");
            }
            if(emptyEmail) {
              $("#inputEmail").addClass("input-error");
            }
            if(emptyPwd) {
              $("#inputPwd").addClass("input-error");
            }
            if(emptyPwdConfirm) {
              $("#inputPwdConfirm").addClass("input-error");
            }
        }
        else if (invalidEmail) {
          $("#inputEmail").addClass("input-error");
        }
        else if (emailTaken) {
          // TODO Doesn't work, this area is never reached from taken email being set
          $("#inputEmail").addClass("input-error");
        }
        else if (invalidPasswordMatch) {
          $("#inputPwd").addClass("input-error");
          $("#inputPwdConfirm").addClass("input-error");
        }
      </script>

      <?php
    }

    // Close connections
    if(isset($stmt)) {
      mysqli_stmt_close($stmt);
    }

    mysqli_close($conn);
}
else {
  //User did not get here through form, send them back
  header("Location: ../index.php");
  exit();
}
?>
