import os
import time
import board
import adafruit_dht
import mysql.connector
from mysql.connector import Error

# Database credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "user")
DB_NAME = os.getenv("DB_NAME", "sensor_data")

# Initialize the DHT22 sensor
dhtDevice = adafruit_dht.DHT22(board.D4)

# Function to insert data into the database
def insert_sensor_data(temperature_c, humidity):
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # SQL insert statement
            sql_query = """
                INSERT INTO temperature_data (timestamp, temperature, humidity)
                VALUES (NOW(), %s, %s);
            """
            cursor.execute(sql_query, (temperature_c, humidity))
            connection.commit()

            print("Datos insertados correctamente en la base de datos.")

    except Error as e:
        print(f"Error de conexión con la base de datos: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

# Function to get multiple readings and calculate the average
def get_average_readings(num_readings=3, delay=2):
    temp_sum, humidity_sum = 0, 0
    valid_readings = 0

    for _ in range(num_readings):
        try:
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity

            if temperature_c is not None and humidity is not None:
                temp_sum += temperature_c
                humidity_sum += humidity
                valid_readings += 1
                print(f"Reading {_ + 1}: Temp: {temperature_c:.1f} C    Humidity: {humidity:.1f}%")
            else:
                print("Failed to read from the sensor.")

        except RuntimeError as error:
            print(f"Sensor error on reading {_ + 1}: {error.args[0]}")

        time.sleep(delay)

    if valid_readings > 0:
        avg_temp = temp_sum / valid_readings
        avg_humidity = humidity_sum / valid_readings
        return avg_temp, avg_humidity
    else:
        raise RuntimeError("No valid readings obtained from the sensor.")

# Main script logic
try:
    # Get average temperature and humidity
    temperature_c, humidity = get_average_readings(num_readings=3, delay=2)

    print(f"Average Temp: {temperature_c:.1f} C    Average Humidity: {humidity:.1f}%")
    # Insert the average data into the database
    insert_sensor_data(temperature_c, humidity)

except RuntimeError as error:
    # Handle errors that occur during sensor reading
    print(f"Sensor error: {error}")

except Exception as error:
    # Handle other exceptions
    dhtDevice.exit()
    print(f"An error occurred: {error}")

finally:
    # Clean up
    dhtDevice.exit()
