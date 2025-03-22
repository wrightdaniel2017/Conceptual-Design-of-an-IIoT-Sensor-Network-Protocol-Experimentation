# IoT: Industrial IoT Sensor Data and Simulation

This repository demonstrates an end-to-end workflow for simulating sensor data via multiple protocols (MQTT, CoAP, and OPC UA) and visualizing the data in real-time. The project provides a robust framework for IoT device simulation and monitoring.

## 📋 Overview

The project includes:
- Sensor simulations for three major IoT protocols:
  - MQTT (Message Queuing Telemetry Transport)
  - CoAP (Constrained Application Protocol)
  - OPC UA (OPC Unified Architecture)
- Built-in MQTT broker for local testing
- Data visualization tools to generate plots of sensor readings
- Multi-process orchestration to run all components simultaneously

## 📑 Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Scripts Overview](#scripts-overview)
- [Data Flow & Visualizations](#data-flow--visualizations)
- [Forecasting Pipeline](#forecasting-pipeline)
- [Optional: VAE-Based Augmentation](#optional-vae-based-augmentation)
- [Logging](#logging)
- [License](#license)

## 🗂️ Project Structure

A simplified view of the folder structure:

```
IoT_L4/
│ 
├── paho.mqtt.python/     # Contains MQTT client libraries or references
├── src/                  # Source code folder
│   ├── coap_sensor_simulation.py
│   ├── data_visualization.py
│   ├── mqtt_sensor_simulation.py
│   └── opcua_sensor_simulation.py
├── visualizations/       # Images and demonstration video
│   ├── coap_visualization.png
│   ├── mqtt_visualization.png
│   ├── opcua_visualization.png
│   └── visualization_demo.mp4
│ 
├── app.log               # Log file (generated after running app.py)
├── app.py                # Main entry point for running all simulations
├── broker.py             # Simple MQTT broker implementation
├── coap_sensor_simulation.py    # Simulates CoAP sensor data
├── data_visualization.py        # Generates visualizations and runs simulations
├── mqtt_sensor_simulation.py    # Simulates MQTT sensor data
├── opcua_sensor_simulation.py   # Simulates OPC UA sensor data
├── readme.md             # Project documentation
└── requirements.txt      # Project dependencies
```

## ✨ Features

### Sensor Protocol Simulations
- **MQTT**: Standard lightweight messaging protocol for IoT, simulating temperature and humidity readings
- **CoAP**: Lightweight HTTP-like protocol optimized for constrained environments
- **OPC UA**: Industrial automation communication protocol with advanced data modeling

### Built-in MQTT Broker
- Simple MQTT broker implementation using hbmqtt
- Automatic broker availability detection before starting simulations

### Data Visualization
- Automatic generation of visualization plots for each protocol
- Real-time data monitoring capabilities
- Sample visualization files created on startup

### Process Management
- Multi-process architecture with robust error handling
- Automatic dependency installation
- Daemon threads for output logging
- Graceful shutdown of all processes

## 🚀 Installation & Setup

1. **Clone the repository** (or download the zip):
   ```bash
   git clone https://github.com/yourusername/IoT_L4.git
   cd IoT_L4
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate (Linux/macOS)
   source .venv/bin/activate
   
   # Activate (Windows)
   .venv\Scripts\activate
   ```

3. **Install required packages**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **(Optional) Set up any required environment variables**:
   - If Nixtla's TimeGPT requires an API key, make sure it is properly set within your scripts or environment.

## 🔧 Usage

### 1. Setup Environment

First, set up your Python environment and install dependencies:

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# OR
.venv\Scripts\activate     # On Windows

# Install dependencies (if not using app.py's auto-installation)
pip install -r requirements.txt
```

### 2. Start the MQTT Broker

Before running the simulations, start the MQTT broker:

```bash
python broker.py
```

This will start a MQTT broker on localhost:1883.

### 3. Run the Application

You can start all simulation components at once using the main application script:

```bash
python app.py
```

This will:
1. Verify all dependencies are installed
2. Check if the MQTT broker is running
3. Start all sensor simulations (MQTT, CoAP, OPC UA)
4. Generate visualization files
5. Monitor and log all processes

### 4. Run Individual Components (Optional)

Alternatively, you can run each component separately:

```bash
# Start MQTT sensor simulation
python mqtt_sensor_simulation.py

# Start CoAP server
python coap_sensor_simulation.py

# Start OPC UA server
python opcua_sensor_simulation.py

# Generate visualizations only
python data_visualization.py
```

### 5. View the Generated Visualizations

After running the application, check the `visualizations/` directory to see the generated plots:
- `mqtt_visualization.png`: MQTT sensor data plot
- `coap_visualization.png`: CoAP sensor data plot
- `opcua_visualization.png`: OPC UA sensor data plot
- `visualization_demo.mp4`: Animated visualization (if FFmpeg is available)

## 📜 Scripts Overview

### `app.py`
- Main entry point for the application
- Orchestrates all simulation components
- Ensures dependencies are installed
- Verifies MQTT broker availability
- Manages process lifecycle and error handling

### `broker.py`
- Implements a simple MQTT broker using hbmqtt
- Listens on 127.0.0.1:1883
- Configured to allow anonymous connections

### `mqtt_sensor_simulation.py`
- Simulates an MQTT sensor publishing temperature and humidity data
- Connects to localhost:1883
- Publishes to "sensor/data" topic with JSON payload
- Updates values every second

### `coap_sensor_simulation.py`
- Implements a CoAP server on port 5683
- Creates a resource at "/sensor" endpoint
- Responds to GET requests with temperature and humidity data in JSON format

### `opcua_sensor_simulation.py`
- Sets up an OPC UA server on port 4840
- Creates variables for temperature and humidity
- Updates values approximately every second
- Makes variables writable for client interaction

### `data_visualization.py`
- Creates visualization plots for all three protocols
- Generates sample visualizations upon startup
- Contains duplicate functionality from app.py for standalone operation
- Creates both static images and a sample animation video

## 📊 Data Flow & Visualizations

1. **Sensor Simulation** → Generates CSV or real-time stream.
2. **Data Preprocessing** (`data_preparation.py`) → Resamples & cleans.
3. **Feature Engineering** (`feature_engineering.py`) → Rolling means, hour-of-day, etc.
4. **Model Training** (`model_training.py`) → Nixtla's TimeGPT forecast.
5. **Evaluation** (`evaluation.py`) → MAE, MSE, error distribution, residual plots.

### Visualizations
- Train/Test Split
- Forecast vs. Actual
- Residuals Over Time
- Error Distribution
- Rolling Statistics

Generated plots are displayed inline or in a pop-up window (depending on your environment). Example images (`coap_visualization.png`, `mqtt_visualization.png`, `opcua_visualization.png`) and a demo video (`visualization_demo.mp4`) are located in the `visualizations/` folder.

## 🛠️ System Architecture

### Communication Flow

The IoT_L4 system uses a multi-process architecture where each component runs independently:

1. **MQTT Flow**:
   - `broker.py` starts a MQTT broker on localhost:1883
   - `mqtt_sensor_simulation.py` connects to the broker and publishes temperature and humidity data
   - Data is published to the "sensor/data" topic in JSON format

2. **CoAP Flow**:
   - `coap_sensor_simulation.py` creates a CoAP server on port 5683
   - The server exposes a "/sensor" resource endpoint
   - Clients can GET sensor data from this endpoint

3. **OPC UA Flow**:
   - `opcua_sensor_simulation.py` sets up an OPC UA server on port 4840
   - The server creates "Temperature" and "Humidity" variables
   - Values are updated regularly and can be read by OPC UA clients

### Process Management

The `app.py` script acts as an orchestrator:

1. **Dependency Management**:
   - Checks for `requirements.txt` and installs required packages
   - Falls back to a hardcoded list of dependencies if the file is missing

2. **Broker Verification**:
   - Checks if an MQTT broker is running on localhost:1883
   - Exits gracefully if no broker is detected

3. **Process Lifecycle**:
   - Starts all sensor simulations as subprocesses
   - Creates daemon threads to capture and log their outputs
   - Monitors process health and handles unexpected terminations
   - Ensures clean shutdown on keyboard interrupt

### Visualization

The `data_visualization.py` script handles the creation of visual assets:

1. **Static Images**:
   - Creates simple plots for each protocol (MQTT, CoAP, OPC UA)
   - Uses matplotlib to generate PNG files

2. **Animation**:
   - Attempts to create an MP4 animation if FFmpeg is available
   - Falls back to creating an empty placeholder file if video generation fails

## 📝 Logging

The application uses Python's built-in logging module to track operations:

- **Log File**: `app.log` is created/appended with each run
- **Console Output**: All log messages are also printed to stdout
- **Log Format**: `%(asctime)s [%(levelname)s] %(message)s`
- **Log Level**: INFO by default

Each sensor simulation process has its output captured and logged with a prefix indicating the source.

## 🛡️ Error Handling

The system includes several error handling mechanisms:

1. **Dependency Management**:
   - Graceful handling of missing packages
   - Detailed error reporting for failed installations

2. **Process Monitoring**:
   - Detection of unexpectedly terminated processes
   - Clean shutdown of all processes on error

3. **Network Connectivity**:
   - Verification of MQTT broker availability
   - Socket timeout handling

## 🧩 Extending the Project

### Adding New Protocols

To add support for a new IoT protocol:

1. Create a new script (e.g., `new_protocol_simulation.py`)
2. Implement the sensor data generation logic
3. Add the script to the `scripts` dictionary in `app.py`

### Customizing Sensor Behavior

Each simulation script can be modified to:

- Change data generation patterns
- Adjust update frequencies
- Add more sensor types beyond temperature and humidity
- Implement error conditions or anomalies

## 📄 License

(Add your preferred license here, e.g., MIT, Apache 2.0, etc.)

---

## 📌 Final Notes

- All simulation scripts are designed to run indefinitely until interrupted
- The MQTT broker must be running before starting the simulations
- For production use, replace the built-in broker with a robust solution like Mosquitto or HiveMQ
- The visualization module requires matplotlib and may need FFmpeg for video generation
- All three protocols (MQTT, CoAP, OPC UA) are standard in IoT applications but serve different use cases

Enjoy exploring multi-protocol IoT sensor simulations!
