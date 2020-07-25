<?php
//File creates a connection to database named $conn that can be used in other files.
$servername = "localhost";
$user = "root";
$password = "";
$database = "soil_mapping";

$conn = mysqli_connect($servername, $user, $password, $database);

if(!$conn) {
    die("Connection failed: ".mysqli_connect_error());
}
?>
