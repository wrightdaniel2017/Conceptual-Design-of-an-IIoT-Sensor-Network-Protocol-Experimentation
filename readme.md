IoT_L4: Industrial IoT Sensor Data and Forecasting
This repository demonstrates an end-to-end workflow for simulating sensor data (via multiple protocols), visualizing the data, and running a forecasting pipeline using TimeGPT (Nixtla) and optional VAE-based data augmentation. The project includes:

Sensor simulations for MQTT, CoAP, and OPC UA
Data visualization scripts to understand sensor readings
Forecasting pipeline (data preparation, feature engineering, model training, evaluation, cross-validation)
Optional VAE-based generative modeling to augment the dataset
Table of Contents
Project Structure
Features
Installation & Setup
Usage
Scripts Overview
Data Flow & Visualizations
Forecasting Pipeline
Optional: VAE-Based Augmentation
Logging
License
Project Structure
A simplified view of the folder structure (see file_structure.txt for more details):


IoT_L4/
│
├── paho.mqtt.python/           # (Optional) Contains MQTT client libraries or references
├── visualizations/             # Images and demonstration video
│   ├── coap_visualization.png
│   ├── mqtt_visualization.png
│   ├── opcua_visualization.png
│   └── visualization_demo.mp4
│
├── app.log                     # Log file (generated after running app.py)
├── app.py                      # Main entry point for the forecasting pipeline
├── coap_sensor_simulation.py   # Simulates CoAP sensor data
├── data_visualization.py       # General data plotting/visualization script
├── file_structure.txt          # Text file describing the directory structure
├── mqtt_sensor_simulation.py   # Simulates MQTT sensor data
├── opcua_sensor_simulation.py  # Simulates OPC UA sensor data
├── requirements.txt            # Project dependencies
└── src/                        # Source code folder (if applicable)
    ├── cross_validation.py
    ├── data_preparation.py
    ├── evaluation.py
    ├── feature_engineering.py
    ├── generative_model.py
    ├── model_training.py
    ├── ...
Features
Sensor Protocol Simulations: Scripts to simulate data publishing via MQTT, CoAP, or OPC UA.
Data Collection & Visualization: Tools to plot raw sensor data, highlighting how the data changes over time.
Forecasting Pipeline:
Data Preparation (resampling, cleaning, handling missing values)
Feature Engineering (rolling means, time-based features)
Model Training using Nixtla’s TimeGPT
Evaluation (MAE, MSE, residual plots, error distributions)
Rolling-Origin Cross-Validation for robust performance metrics
Generative Modeling (Optional): Variational Autoencoder (VAE) to create synthetic sensor data and augment the dataset for improved forecasting.
Visual Reports: Automatic generation of plots (actual vs. forecast, residuals, rolling statistics, etc.)
Installation & Setup
Clone the repository (or download the zip):


git clone https://github.com/yourusername/IoT_L4.git
cd IoT_L4
Create and activate a virtual environment (recommended):


python -m venv .venv
source .venv/bin/activate       # On Linux/macOS
.venv\Scripts\activate          # On Windows
Install required packages:


pip install --upgrade pip
pip install -r requirements.txt
(Optional) Set up any required environment variables:

If Nixtla’s TimeGPT requires an API key, make sure it is properly set within your scripts or environment.
Usage
Below is a high-level workflow. Adjust paths and flags as needed:

1. Simulate Sensor Data
You can run any of the sensor simulation scripts to generate or publish data:


# CoAP sensor simulation
python coap_sensor_simulation.py

# MQTT sensor simulation
python mqtt_sensor_simulation.py

# OPC UA sensor simulation
python opcua_sensor_simulation.py
Each script may output data to a file, console, or a local broker/server, depending on your configuration.

2. Visualize Sensor Data
To quickly plot or analyze the generated sensor data (for example, saved in a CSV or in-memory), run:


python data_visualization.py
This script may produce plots like real-time line charts or static graphs saved to disk (depending on your configuration).

3. Run the Forecasting Pipeline
The main entry point for training and forecasting is app.py. It includes:

Data loading/preprocessing
Feature engineering
Model training (TimeGPT)
Evaluation & cross-validation
(Optional) VAE-based data augmentation
Run the pipeline with:


python app.py
Optional Flags:

--augment: Enables the VAE-based augmentation step.
--data <path>: Override the default data path if needed.
--vae_epochs <int> and --vae_batch_size <int>: Control training parameters for the VAE.
Example:


python app.py --augment --vae_epochs 15 --vae_batch_size 64
Scripts Overview
app.py

Orchestrates the entire pipeline.
Calls data preparation, feature engineering, model training, evaluation, and cross-validation.
Handles optional VAE-based augmentation.
coap_sensor_simulation.py, mqtt_sensor_simulation.py, opcua_sensor_simulation.py

Generate or publish sensor data using the respective protocol.
May require additional configuration (e.g., specifying broker addresses, ports, etc.).
data_visualization.py

Plots the sensor data (e.g., line charts, scatter plots).
Helps you quickly see how data changes over time.
requirements.txt

Lists Python dependencies (e.g., paho-mqtt, nixtla, matplotlib, pandas, tensorflow, etc.).
src/data_preparation.py

Loads and preprocesses the sensor data (resampling, handling missing values, etc.).
src/feature_engineering.py

Adds new features (e.g., rolling means, time-based features like hour of the day).
src/model_training.py

Trains a forecasting model with Nixtla’s TimeGPT, including exogenous features.
src/evaluation.py

Evaluates forecast performance (MAE, MSE).
Handles custom logic for retrieving forecast columns.
src/cross_validation.py

Performs rolling-origin cross-validation for time-series data.
Splits data into multiple train/test folds over time.
src/generative_model.py

Contains the VAE (Variational Autoencoder) logic for generating synthetic sensor data.
Data Flow & Visualizations
Sensor Simulation → Generates CSV or real-time stream.
Data Preprocessing (data_preparation.py) → Resamples & cleans.
Feature Engineering (feature_engineering.py) → Rolling means, hour-of-day, etc.
Model Training (model_training.py) → Nixtla’s TimeGPT forecast.
Evaluation (evaluation.py) → MAE, MSE, error distribution, residual plots.
Visualizations
Train/Test Split
Forecast vs. Actual
Residuals Over Time
Error Distribution
Rolling Statistics
Generated plots are displayed inline or in a pop-up window (depending on your environment). Example images (coap_visualization.png, mqtt_visualization.png, opcua_visualization.png) and a demo video (visualization_demo.mp4) are located in the visualizations/ folder.

Forecasting Pipeline
When you run:


python app.py
The pipeline steps are:

Load & Preprocess: Reads your CSV (e.g., IOT-temp.csv), handles missing data, sets frequency, etc.
Feature Engineering: Adds custom features (rolling mean, time-based features).
Train & Forecast: Calls Nixtla’s TimeGPT to forecast future values.
Evaluation: Compares predicted values vs. actual values in the test set.
Rolling-Origin CV: Splits your time series multiple times for robust evaluation.
(Optional) VAE Augmentation: Trains a VAE on the dataset, generates synthetic data, appends to the original dataset, and re-trains.
Outputs:

Forecast: Printed to console and optionally saved as forecast_output.csv.
Plots: Various plots (actual vs. forecast, residuals, distribution, etc.)
Log: Detailed log written to app.log.
Optional: VAE-Based Augmentation
If you enable the --augment flag, the pipeline will:

Train a VAE on your existing dataset (based on vae_epochs and vae_batch_size).
Generate synthetic sensor readings (same distribution as your real data).
Append synthetic data to the real dataset.
Retrain the forecasting model on this augmented dataset.
Evaluate again to see if performance improves.
Logging
app.log: After each run of app.py, a detailed log is appended or created.
Log details: Each pipeline step, including data loading, model training, evaluation metrics, and cross-validation folds.
License
(Add your preferred license here, e.g., MIT, Apache 2.0, etc.)

Final Notes
For best performance, ensure you have enough historical data for training and a reasonable forecast horizon.
If you see warnings about exogenous features or forecast horizon from Nixtla, you can fine-tune the hist_exog_list or reduce the forecast h.
Customize each sensor simulation script to match your real-world broker configurations or data endpoints.
If you have any questions or need further modifications, feel free to reach out!

Enjoy exploring your IoT sensor data and building advanced forecasting models!