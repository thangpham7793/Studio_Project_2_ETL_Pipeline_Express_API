<?php
// Check if user is already logged in, display logout button if so
if (isset($_SESSION['userID'])) {
  echo '
  <p class="welcome">Hello '.$_SESSION['firstName'].'</p>
  <form class="form-inline" action="includes/logout.inc.php" method="post"">
    <button type="submit" name="logout-submit" class="btn btn-primary mb-2">Logout</button>
  </form>';
}
else {
  // Not logged in, show signup button and login form
  echo '
  <form id="formLogin" class="form-inline" action="includes/login.inc.php" method="post">
    <input type="text" name="email" class="form-control mb-2 mr-sm-2" id="inputLoginEmail" placeholder="Email...">

    <div class="input-group mb-2 mr-sm-2">
      <input type="password" name="pwd" class="form-control" id="inputLoginPassword" placeholder="Password...">
    </div>
    <button type="submit" name="login-submit" class="btn btn-primary mb-2 login">Login</button>
  </form>
  <button type="button" class="btn btn-primary mb-2 signup" data-toggle="modal" data-target="#modal_signup">
    Sign up
  </button>';
}

 ?>
