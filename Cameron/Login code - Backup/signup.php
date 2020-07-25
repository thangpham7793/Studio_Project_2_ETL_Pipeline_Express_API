<h1>Sign up</h1>
<?php
  if (isset($_GET['error'])) {
    if(isset($_GET['firstName'])) {
      $firstName = $_GET['firstName'];
    }
    else {
      $firstName = "";
    }
    if(isset($_GET['surname'])) {
      $surname = $_GET['surname'];
    }
    else {
      $surname = "";
    }
    if(isset($_GET['email'])) {
      $email = $_GET['email'];
    }
    else {
      $email = "";
    }

    if($_GET['error'] == "emptyfields") {
      echo '<p>Fill in all fields!</p>';
    }
    else if ($_GET['error'] == "invalidinputs") {
      echo '<p>Invalid name and email</p>';
    }
    else if ($_GET['error'] == "invalidmail") {
      echo '<p>Invalid email!</p>';
    }
    else if ($_GET['error'] == "invalidname") {
      echo '<p>Invalid name!</p>';
    }
    else if ($_GET['error'] == "passwordCheck") {
      echo '<p>Passwords do not match!</p>';
    }
    else if ($_GET['error'] == "emailtaken") {
      echo '<p>Email is already used!</p>';
    }
  }
  else if ($_GET['signup'] == "success") {
    echo '<p>Signup successful</p>';
  }

 ?>
<form action="includes/signup.inc.php" method="post">
    <input type="text" name="firstName" value="<?php echo $firstName ?>" placeholder="First Name...">
    <input type="text" name="surname" value="<?php echo $surname ?>" placeholder="Surname...">
    <input type="text" name="email" value="<?php echo $email ?>" placeholder="Email Address...">
    <input type="password" name="pwd" placeholder="Password...">
    <input type="password" name="pwd-confirm" placeholder="Repeat Password...">
    <button type="submit" name="signup-submit">Sign up</button>
</form>
