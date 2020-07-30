<?php
$host = "localhost";
$userMS = "root";
$passwordMS = "";
$database = "soil_mapping";
$connection = mysqli_connect($host,$userMS,$passwordMS,$database);

if(!$connection){
	die("Connection failed: " . mysqli_connect_error());
}

$sql = "CREATE TABLE IF NOT EXISTS user (
userID INT AUTO_INCREMENT PRIMARY KEY,
firstName TEXT NOT NULL,
surname TEXT NOT NULL,
email TEXT NOT NULL,
password LONGTEXT NOT NULL
)";
echo("creating user table");
echo("<br>");

if(mysqli_query($connection,$sql)) {
	echo "User table created successfully";
	echo("<br>");
} else {
	echo "Error creating table: " . mysqli_error($connection);
	echo("<br>");
}

$sql = "CREATE TABLE IF NOT EXISTS request (
requestID INT AUTO_INCREMENT PRIMARY KEY,
userID INT NOT NULL FOREIGN KEY,
supplierID INT NOT NULL,
supplierName TEXT NOT NULL,
supplierContact TEXT NOT NULL,
material TEXT NOT NULL,
deliveryAddress TEXT NOT NULL
)";
echo("creating request table");
echo("<br>");

if(mysqli_query($connection,$sql)) {
	echo "Request table created successfully";
	echo("<br>");
} else {
	echo "Error creating table: " . mysqli_error($connection);
	echo("<br>");
}

mysqli_close($connection);
?>
