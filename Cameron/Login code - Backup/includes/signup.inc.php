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

    //Check for errors in info
    if(empty($firstName) || empty($surname) || empty($email) || empty($password) || empty($passwordConfirm)) {
        header("Location: ../index.php?error=emptyfields&firstName=".$firstName."&surname=".$surname."&email=".$email);
        exit();
    }
    else if(!filter_var($email, FILTER_VALIDATE_EMAIL) && (!preg_match("/^[a-zA-Z0-9]*$/", $firstName)) || !preg_match("/^[a-zA-Z0-9]*$/", $surname)) {
        header("Location: ../index.php?error=invalidinputs");
        exit();
    }
    else if(!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        header("Location: ../index.php?error=invalidmail&firstName=".$firstName."&surname=".$surname);
        exit();
    }
    else if(!preg_match("/^[a-zA-Z0-9]*$/", $firstName) || !preg_match("/^[a-zA-Z0-9]*$/", $surname)) {
        header("Location: ../index.php?error=invalidname&email=".$email);
        exit();
    }
    else if($password !== $passwordConfirm) {
        header("Location: ../index.php?error=passwordCheck&firstName=".$firstName."&surname=".$surname."&email=".$email);
        exit();
    }
    else {
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
            header("Location: ../index.php?error=emailtaken");
            exit();
          }
          else {
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
              header("Location: ../index.php?signup=success");
              exit();
            }
          }
        }
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
