# Whitefly Early Detection and Environmental Monitoring System for Greenhouses (Master's Thesis)


Click below to acces a Colab notebook for training YOLO models. It makes training a custom YOLO model as easy as uploading an image dataset and running a few blocks of code.

<a href="https://colab.research.google.com/drive/1YRTQBoLqL1gWWpOXaxf411O2vtJRf_y8?usp=sharing" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Overview

This repository contains the source code, models, and documentation for the Final Master's Project (TFM) focused on the design and implementation of a low-cost system for **real-time environmental monitoring (temperature and humidity) and automated early detection of the whitefly (*Bemisia tabaci*)** in greenhouses.

The system combines accessible hardware (Raspberry Pi 5, sensors, camera) with open-source software (Python, Docker, Deep Learning) to create a scalable and accessible solution aimed at improving integrated pest management and optimizing growing conditions.

## Key Features and Goals

* **Early Whitefly Detection:** Utilizes Deep Learning models (CNNs) to identify the presence of whiteflies in images captured in real-time.
* **Environmental Monitoring:** Continuously measures greenhouse temperature and humidity using a DHT22 sensor.
* **Low-Cost System:** Employs affordable hardware components and open-source software.
* **Automation:** Uses CRON for periodic and automated acquisition of environmental data.
* **Data Storage:** Saves historical sensor data and detection results in a MySQL database.
* **Web Visualization:** Offers a web interface to monitor environmental conditions (historical graphs) and view the camera's video stream with superimposed detections.
* **Containerized Architecture:** Uses Docker to encapsulate web and database services, facilitating deployment and reproducibility.
* **Scalability:** Designed with modular components allowing for future expansion.

## System Architecture

<p align=center>
<img src="https://raw.githubusercontent.com/ialvarenga08/TFM_Deteccion_Mosca_Blanca/main/Assets/media/Diagrama_De_Bloques_4.png" height="380"><br>
<i>Example of a whiteflie image labeled with Label Studio.</i>
</p>

**Main Components:**

1.  **Hardware:**
    * **Central Unit:** Raspberry Pi 5 (8GB RAM, OS: Raspberry Pi OS / Debian Bookworm).
    * **Environmental Sensor:** DHT22 (Temperature and Humidity).
    * **Camera:** Raspberry Pi Camera Module 3.
2.  **Software:**
    * **Docker Containers:**
        * **Web Server:** Apache2 + PHP.
        * **Database:** MySQL.
    * **Python Scripts:**
        * `sensor.py`: Acquires data from DHT22 and inserts it into MySQL (run by CRON).
        * `stream_detection.py` (or similar): Flask script to capture video, run the detection model (YOLOv11s/SSD), and serve the processed stream (runs outside Docker).
    * **Web Interface:** HTML, CSS, JavaScript (with Chart.js).
    * **Automation:** CRON.
3.  **AI Model:**
    * Object detection model (YOLOv11s or SSD MobileNetV1) trained on Google Colab.
    * Custom dataset annotated with LabelImg.

## Technology Stack

* **Hardware:** Raspberry Pi 5, DHT22, Raspberry Pi Camera Module 3
* **Operating System:** Raspberry Pi OS (Debian Bookworm)
* **Languages:** Python, PHP, JavaScript, HTML, CSS, SQL, Bash
* **Frameworks/Libraries:**
    * **Python:** Ultralytics (YOLO), TensorFlow/TensorFlow Lite (SSD), Flask, OpenCV, picamera2, adafruit-dht, mysql-connector-python, NumPy
    * **JavaScript:** Chart.js, chartjs-adapter-date-fns
* **Containerization:** Docker, Docker Compose
* **Database:** MySQL
* **Web Server:** Apache2
* **Automation:** CRON

## Requirements

**Hardware:**

* Raspberry Pi 5 (8GB RAM recommended)
* microSD Card (minimum 16GB, Class 10 or higher recommended)
* Appropriate Power Supply for Raspberry Pi 5
* DHT22 Sensor
* Raspberry Pi Camera Module 3 with its ribbon cable
* Jumper wires
* (Optional but recommended) 4.7kΩ to 10kΩ Pull-up resistor for DHT22

**Software (on the Raspberry Pi):**

* Raspberry Pi OS (Bookworm - 64-bit recommended)
* Docker and Docker Compose
* Python 3.x
* Git
* Required Python libraries for the streaming script (`stream_detection.py`) installed on the *host*:
    * `pip install flask opencv-python ultralytics Pillow picamera2 libatlas-base-dev` (Adjust based on the final model and exact dependencies)
    * *Note:* May require additional configuration for `picamera2` on Bookworm.

## Installation and Setup

1.  **Initial Raspberry Pi Setup:**
    * Install Raspberry Pi OS (Bookworm - 64-bit recommended) on the microSD card.
    * Configure network connection (Wi-Fi or Ethernet).
    * Enable the Camera interface and I2C/SPI interface (if needed for the sensor) using `sudo raspi-config`.
    * Update the system: `sudo apt update && sudo apt upgrade -y`.

2.  **Install Required Software (Host):**
    * Install Git: `sudo apt install git -y`
    * Install Docker and Docker Compose (follow the [official Docker guide](https://docs.docker.com/engine/install/debian/) for Raspberry Pi OS). Add your user (e.g., `pi`) to the `docker` group: `sudo usermod -aG docker $USER` (requires logout/reboot).
    * Install Python 3 and pip (usually included with Raspberry Pi OS).
    * Install the necessary Python libraries for the streaming script *outside* the container (see "Software Requirements").

3.  **Clone Repository:**
    ```bash
    git clone [URL-OF-YOUR-REPOSITORY]
    cd [CLONED-DIRECTORY-NAME]
    ```

4.  **Hardware Setup:**
    * Connect the DHT22 sensor to the Raspberry Pi GPIO pins (VCC to 3.3V pin 1, DATA to GPIO 4 pin 7, GND to Ground pin 9). *Ensure you use the pull-up resistor between DATA and VCC.*
    * Connect the Camera Module 3 to the CSI port on the Raspberry Pi.

5.  **Docker Setup:**
    * Review/Create the `docker-compose.yml` file. This file will define the Apache/PHP and MySQL services. (Including a `docker-compose.yml` in the repository is recommended).
    * Build and run the containers:
        ```bash
        docker-compose up --build -d
        ```
    * **Database:** The first time it runs, the MySQL container should create the database (`sensor_data`) and table (`temperature_data`) as defined in initialization scripts or the MySQL Dockerfile. You might need to manually run an SQL script to create the table if not automated. Configure database credentials (user, password) securely (preferably using environment variables in `docker-compose.yml`).

6.  **Python Script Configuration:**
    * **`sensor.py`:** Ensure the database credentials within this script match those configured for the MySQL container (ideally, read them from environment variables or a config file). Place this script in the appropriate path (e.g., `/var/www/html/` if run from the Apache container, or another location if run from the host).
    * **`stream_detection.py` (or similar):**
        * Ensure it has the trained model (`.pt` or `.tflite`) and the `labelmap.txt` file in an accessible location. *(Recommendation: Include the final model in the repository or provide a download link)*.
        * Verify the paths to the model and labelmap within the script.
        * This script runs on the *host*, not inside Docker.

7.  **CRON Setup:**
    * Open the crontab editor: `crontab -e`
    * Add the line to execute `sensor.py` at regular intervals (e.g., every 4 hours):
        ```cron
        0 2,6,10,14,18,22 * * * /usr/bin/python3 /full/path/to/sensor.py >> /path/to/some/log.log 2>&1
        ```
        * *(Ensure you use the correct full path to your `sensor.py` script and consider redirecting output to a log file)*.

8.  **Web Interface Configuration:**
    * Ensure the PHP, HTML, CSS, and JS files are in the correct directory served by Apache (usually `/var/www/html/` inside the Apache container).
    * Verify that the PHP script (`Workspace_data.php`) uses the correct credentials to connect to the MySQL database (using the service name defined in `docker-compose.yml` as the host).
    * Verify that the `<img>` tag in the HTML file points to the **local IP address of the Raspberry Pi** and port 5000 (or the port configured in Flask): `src="http://<RASPBERRY_PI_IP>:5000/video_feed"`.

## Usage

1.  **Start Docker Services:** If the containers are not running, start them:
    ```bash
    cd [PATH-TO-DIRECTORY-WITH-DOCKER-COMPOSE]
    docker-compose up -d
    ```
2.  **Start Streaming Script:** Run the Flask script in a separate terminal on the Raspberry Pi:
    ```bash
    python3 /full/path/to/stream_detection.py
    ```
    *(Running it in the background using `nohup` or `screen`/`tmux` can be useful)*.
3.  **Access Web Interface:** Open a web browser on a device connected to the same network as the Raspberry Pi and navigate to `http://<RASPBERRY_PI_IP>`.
4.  **Monitoring:** The web interface will display the temperature/humidity graphs and the video stream with detections. Data should update automatically (graphs via AJAX/fetch, video via streaming). Environmental data acquisition runs in the background via CRON.

## Model Training

The object detection models (SSD MobileNetV1/V2, YOLOv11s) were trained using Google Colab. The detailed training notebooks can be found in the `/notebooks` (or similar) folder of this repository.

* **Dataset:** A custom dataset of whitefly images was used, annotated with LabelImg.
* **Models:** SSD MobileNetV2 FPN Lite, SSD MobileNetV1, and YOLOv11s were experimented with. The final model selected for deployment was [State your final model: SSD MobileNetV1 640x640 or YOLOv11s (Training 1)].
* **Results:** Refer to the TFM report for a detailed analysis of performance metrics (mAP, Precision, Recall).

## License

This project is distributed under the [Choose a license, e.g., MIT, Apache 2.0] License. See the `LICENSE` file for more details.

## Acknowledgements

* To [Universidad Politecnica de Cartagena] and my TFM advisor(s), [Pr.Pablo Matencio ], for their guidance and support.
* To the open-source communities behind Python, TensorFlow, Ultralytics, Docker, Raspberry Pi, OpenCV, Flask, Chart.js, and other libraries used.
  

## Contact

[Imer Alvarenga] - [https://www.linkedin.com/in/imeralvarenga/]
