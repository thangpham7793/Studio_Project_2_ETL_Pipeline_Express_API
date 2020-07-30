<?php
// Check user got here through submit button
if (isset($_POST['login-submit'])) {
    // Get connection to database
    require 'dbh.inc.php';

    // Collect login info from previous page
    $email = $_POST['email'];
    $password = $_POST['pwd'];

    // If no values, send user back and stop running code
    if (empty($email) || empty($password)) {
      header("Location: ../index.php?error=emptyfields");
      exit();
    }
    else {
      // '?' is a standin that is replaced during binding
      $sql = "SELECT * FROM user WHERE email=?";
      $stmt = mysqli_stmt_init($conn);

      // Send prepared statement to server
      if (!mysqli_stmt_prepare($stmt, $sql)) {
        header("Location: ../index.php?error=sqlerror");
        exit();
      }
      else {
        // Bind parameters to statement
        mysqli_stmt_bind_param($stmt, "s", $email);
        // Run statement
        mysqli_stmt_execute($stmt);
        $result = mysqli_stmt_get_result($stmt);

        // Get result as an associative(named keys) array
        if ($row = mysqli_fetch_assoc($result)) {
          // Check that the hashed password matches one in DB
          $pwdCheck = password_verify($password, $row['password']);
          if ($pwdCheck == false) {
            header("Location: ../index.php?error=wrongpassword");
            exit();
          }
          else if ($pwdCheck == true) {
            // Login info correct - start session so we know user is logged in
            session_start();
            $_SESSION['userID'] = $row['userID'];
            $_SESSION['firstName'] = $row['firstName'];

            header("Location: ../index.php?login=success");
            exit();
          }
          else {
            header("Location: ../index.php?error=wrongpassword");
            exit();
          }
        }
        else {
          header("Location: ../index.php?error=nouser");
          exit();
        }
      }
    }

    mysqli_stmt_close($stmt);
    mysqli_close($conn);
  }
  else {
    // User did not get here through form, send them back
    header("Location: ../index.php");
    exit();
  }
 ?>
