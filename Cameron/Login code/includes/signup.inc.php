<?php
// Check user got here from signup form
if (isset($_POST['signup-submit'])) {
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

    $invalidEmail = false;
    if(!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $invalidEmail = true;
    }

    $invalidPasswordMatch = false;
    if($password !== $passwordConfirm) {
        $invalidPasswordMatch = true;
    }

    // Check if all inputs are valid
    if(!$emptyFirstName && !$emptySurname && !$emptyPwd && !$emptyPwdConfirm && !$invalidEmail && !$invalidPasswordMatch) {
        // '?' is a standin that is replaced during binding
        // Following code checks if email already exists in DB
        $sql = "SELECT email FROM user WHERE email=?";
        $stmt = mysqli_stmt_init($conn);

        // Send prepared statement to server
        if(!mysqli_stmt_prepare($stmt, $sql)) {
          header("Location: ../index.php?error=sqlerror");
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
          }
          else {
            if(!$emailTaken) {
              // Fresh user, prepare SQL. '?' is a standin that is replaced during binding
              $sql = "INSERT INTO user(firstName, surname, email, password) VALUES(?,?,?,?)";
              $stmt = mysqli_stmt_init($conn);

              //Send prepared statement to server
              if (!mysqli_stmt_prepare($stmt, $sql)) {
                header("Location: ../index.php?error=sqlerror");
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

                ?>

                <script>
                  var signupSuccess = "<?php echo $signupSuccess ?>";

                  if(signupSuccess) {
                    $(".submit-feedback").val("Signup successful");
                  }
                </script>

                <?php
              }
            }
          }
        }
    }
    else {
      ?>
      <script>
        var emptyFirstName = "<?php echo $emptyFirstName ?>";
        var emptySurname = "<?php echo $emptySurname ?>";
        var emptyEmail = "<?php echo $emptyEmail ?>";
        var emptyPwd = "<?php echo $emptyPwd ?>";
        var emptyPwdConfirm = "<?php echo $emptyPwdConfirm ?>";
        var emailTaken = "<?php echo $emailTaken ?>";
        var invalidEmail = "<?php echo $invalidEmail ?>";
        var invalidPasswordMatch = "<?php echo $invalidPasswordMatch ?>";

        if(emptyFirstName || emptySurname || emptyEmail || emptyPwd || emptyPwdConfirm) {
          $(".submit-feedback").val("Please fill all fields");
        }
        else if (invalidEmail) {
          $(".submit-feedback").val("Invalid email");
        }
        else if (emailtaken) {
          $(".submit-feedback").val("Email taken");
        }
        else if (invalidPasswordMatch) {
          $(".submit-feedback").val("Passwords do not match");
        }
      </script>

      <?php
    }

    // Close connections
    mysqli_stmt_close($stmt);
    mysqli_close($conn);
}
else {
  // User did not get here through form, send them back
  header("Location: ../index.php");
  exit();
}
?>
