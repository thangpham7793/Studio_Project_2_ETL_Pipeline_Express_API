<?php
session_start();
 ?>

 <!doctype html>
 <html lang="en">
     <head>
         <!-- Required meta tags -->
         <meta charset="utf-8">
         <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

         <script
          src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"
          integrity="sha512-gZwIG9x3wUXg2hdXF6+rVkLF/0Vi9U8D2Ntg4Ga5I5BZpVkVxlJWbSQtXPSiUTtC0TjtGOmxa1AJPuV0CPthew=="
          crossorigin=""
        ></script>
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
          integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
          crossorigin=""
        />

         <!-- Bootstrap CSS -->
         <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
         <link rel="stylesheet" type="text/css" href="style.css">
         <link rel="stylesheet" href="index.css" />
         <title>Soil Mapping</title>
     </head>
     <body>
       <header>
          <nav class="navbar navbar-expand-lg navbar_custom">
            <a class="navbar-brand" href="#">
              <img id="logo" src="images/alliance_logo.png" alt="logo">
            </a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse allign_right" id="navbarSupportedContent">
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
                  <form class="form-inline" action="includes/login.inc.php" method="post">
                    <label class="sr-only" for="inlineFormInputName2">Name</label>
                    <input type="text" name="email" class="form-control mb-2 mr-sm-2" id="inlineFormInputName2" placeholder="Email...">

                    <label class="sr-only" for="inlineFormInputGroupUsername2">Username</label>
                    <div class="input-group mb-2 mr-sm-2">
                      <input type="password" name="pwd" class="form-control" id="inlineFormInputGroupUsername2" placeholder="Password...">
                    </div>
                    <button type="submit" name="login-submit" class="btn btn-primary mb-2">Login</button>
                  </form>
                  <button type="button" class="btn btn-primary mb-2 signup" data-toggle="modal" data-target="#modal_signup">
                    Sign up
                  </button>';
                }
               ?>
            </div>
          </nav>

       </header>

       <!-- Modal -->
       <div class="modal fade" id="modal_signup">
         <div class="modal-dialog">
           <div class="modal-content">
             <div class="modal-header">
               <h5 class="modal-title" id="exampleModalLabel">Signup!</h5>
               <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                 <span aria-hidden="true">&times;</span>
               </button>
             </div>

             <!-- Signup modal -->
             <form action="includes/signup.inc.php" method="post">
             <div class="modal-body">
                  <div class="form-row">
                    <div class="form-group col-md-6">
                      <label for="inputFirstName">First Name</label>
                      <input type="text" name="firstName" class="form-control" id="inputFirstName" placeholder="First name...">
                    </div>
                    <div class="form-group col-md-6">
                      <label for="inputSurname">Surname</label>
                      <input type="text" name="surname" class="form-control" id="inputSurname" placeholder="Surname...">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="inputEmail">Email Address</label>
                    <input type="text" name="email" class="form-control" id="inputEmail" placeholder="Email...">
                  </div>
                  <div class="form-group">
                    <label for="inputPwd">Password</label>
                    <input type="password" name="pwd" class="form-control" id="inputPwd" placeholder="Password...">
                  </div>
                  <div class="form-group">
                    <label for="inputPwdConfirm">Confirm Password</label>
                    <input type="password" name="pwdConfirm" class="form-control" id="inputPwdConfirm" placeholder="Confirm Password...">
                  </div>
                  <p id="submit-feedback"></p>
             </div>
             <div class="modal-footer">
               <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
               <button type="submit" name="signup-submit" class="btn btn-primary">Submit</button>
             </div>
             </form>
           </div>
         </div>
       </div>
