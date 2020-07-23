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
echo("creating table");

if(mysqli_query($connection,$sql)) {
	echo "User table created successfully";
} else {
	echo "Error creating table: " . mysqli_error($connection);
}

mysqli_close($connection);
?>
