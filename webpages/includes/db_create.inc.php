<?php
$host = "localhost";
$userMS = "root";
$passwordMS = "";
$connection = mysqli_connect($host,$userMS,$passwordMS);

if(!$connection){
	die("Connection failed: " . mysqli_connect_error());
}

$dbError = false;

// Try to create database called soil_mapping
echo "Creating database soil_mapping";
echo "<br>";
$sql = "CREATE DATABASE IF NOT EXISTS soil_mapping";
if(mysqli_query($connection,$sql)) {
	echo "Database created";
	echo "<br>";
} else {
	echo "Error creating database: " . mysqli_error($connection);
	echo "<br>";
	$dbError = true;
}
mysqli_close($connection);


// Create tables if no database creation error
if(!$dbError) {
	// Connect to database
	$dbName = 'soil_mapping';
	$connection = mysqli_connect($host,$userMS,$passwordMS, $dbName);

	if(!$connection){
		die("Connection failed: " . mysqli_connect_error());
	}

	// Query for user table
	$sql = "CREATE TABLE IF NOT EXISTS user (
	userID INT AUTO_INCREMENT PRIMARY KEY,
	firstName TEXT NOT NULL,
	surname TEXT NOT NULL,
	email TEXT NOT NULL,
	password LONGTEXT NOT NULL
	)";
	echo "creating user table";
	echo "<br>";

	// Display if successful or not
	if(mysqli_query($connection,$sql)) {
		echo "User table created successfully";
		echo "<br>";
	} else {
		echo "Error creating table: " . mysqli_error($connection);
		echo "<br>";
	}

	// Query for request table
	// TODO supplier details in separate table
	$sql = "CREATE TABLE IF NOT EXISTS request (
	requestID INT AUTO_INCREMENT PRIMARY KEY,
	userFirstName TEXT NOT NULL,
	userSurname TEXT NOT NULL,
	userPhone TEXT NOT NULL,
	userEmail TEXT NOT NULL,
	deliveryAddress TEXT NOT NULL,
	materials TEXT NOT NULL,
	addDetails TEXT NOT NULL,
	supplierID TEXT NOT NULL,
	supplierMineName TEXT NOT NULL,
	supplierControllerName TEXT NOT NULL,
	supplierOperatorName TEXT NOT NULL,
	supplierNearestTown TEXT NOT NULL,
	supplierCoordinates TEXT NOT NULL,
	pending BOOLEAN NOT NULL,
	completed BOOLEAN NOT NULL
	)";
	echo("creating request table");
	echo("<br>");

	// Display is successful or not
	if(mysqli_query($connection,$sql)) {
		echo "Request table created successfully";
		echo "<br>";
	} else {
		echo "Error creating table: " . mysqli_error($connection);
		echo "<br>";
	}

	mysqli_close($connection);
}
?>
