<?php
date_default_timezone_set('Europe/Madrid');
// Database credentials
$host = "db"; // Use "db" because it's the service name in Docker Compose
$username = "user";
$password = "user";
$database = "sensor_data";

// Set the content type to JSON
header('Content-Type: application/json');

// Enable error reporting for debugging (remove in production)
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

try {
    // Create a new MySQLi connection
    $conn = new mysqli($host, $username, $password, $database);

    // Check for connection errors
    if ($conn->connect_error) {
        throw new Exception("Connection failed: " . $conn->connect_error);
    }

    // Query to fetch whiteflies detection data
    $query = "SELECT timestamp, cantidad_moscas, imagen_path 
              FROM detecciones_mosca_blanca 
              WHERE cantidad_moscas > 0 
              ORDER BY timestamp DESC 
              LIMIT 50"; // Limit to the last 50 detections for performance

    $result = $conn->query($query);

    if (!$result) {
        throw new Exception("Query failed: " . $conn->error);
    }

    // Array to store the data
    $data = [];

    // Fetch the data and format it
    while ($row = $result->fetch_assoc()) {
        $data[] = [
            'timestamp' => $row['timestamp'], // e.g., "2025-03-28 10:44:38"
            'count' => (int)$row['cantidad_moscas'], // e.g., 4
            'image_url' => $row['imagen_path'] // e.g., "detection_images/detection_20250328_114438_086b2324.jpg"
        ];
    }

    // Close the result set and connection
    $result->free();
    $conn->close();

    // Output the JSON data
    echo json_encode($data);

} catch (Exception $e) {
    // Output an error message in JSON format
    http_response_code(500); // Set HTTP status code to 500 (Internal Server Error)
    echo json_encode(['error' => $e->getMessage()]);
}
?>
