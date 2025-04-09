<?php
// Database credentials
$host = "db"; // Use "db" because it's the service name in Docker Compose
$username = "user";
$password = "user";
$database = "sensor_data";

// Connect to the database
$conn = new mysqli($host, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die(json_encode(["error" => "Connection failed: " . $conn->connect_error]));
}

// Fetch data from the database
$sql = "SELECT timestamp, temperature, humidity FROM temperature_data ORDER BY timestamp DESC LIMIT 100";
$result = $conn->query($sql);

$data = [];
if ($result->num_rows > 0) {
    // Fetch rows as associative arrays
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
}

// Output the data in JSON format
header('Content-Type: application/json');
echo json_encode($data);

// Close the database connection
$conn->close();
?>
