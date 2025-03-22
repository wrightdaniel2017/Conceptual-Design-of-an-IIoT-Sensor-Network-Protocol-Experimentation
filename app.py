import subprocess
import logging
import sys
import threading
import time
import os
import socket

def setup_logging():
    # Configure logging to output to both the console and a log file.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def ensure_dependencies():
    """
    Ensure all required dependencies are installed.
    If a 'requirements.txt' file exists, it will be used.
    Otherwise, each package is installed individually.
    The dependencies list now includes numpy (pinned to 1.24.3)
    to avoid binary incompatibility issues with pandas.
    """
    if os.path.exists("requirements.txt"):
        logging.info("Found requirements.txt. Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        except subprocess.CalledProcessError as e:
            logging.error("Failed to install dependencies from requirements.txt: " + str(e))
            sys.exit(1)
    else:
        logging.info("requirements.txt not found. Installing individual dependencies...")
        dependencies = [
            "paho-mqtt==2.1.0",
            "aiocoap==0.4.7",
            "asyncua==1.0.1",
            "pandas==2.1.0",
            "numpy==1.24.3",  # Added to fix binary incompatibility issues
            "matplotlib==3.7.2"
        ]
        for dep in dependencies:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to install {dep}: " + str(e))
                sys.exit(1)

def check_mqtt_broker(host="localhost", port=1883, timeout=3):
    """
    Check if an MQTT broker is running by attempting to open a socket connection.
    Returns True if successful, False otherwise.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

def start_process(script_name):
    logging.info(f"Starting {script_name}...")
    # Use sys.executable to ensure the current Python interpreter (with installed dependencies) is used.
    process = subprocess.Popen(
        [sys.executable, script_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    return process

def log_output(process, name):
    # Continuously read the process output and log it.
    for line in iter(process.stdout.readline, ''):
        if line:
            logging.info(f"{name}: {line.strip()}")
    process.stdout.close()

def main():
    setup_logging()
    ensure_dependencies()
    
    # Check for MQTT broker availability before starting simulations.
    if not check_mqtt_broker():
        logging.error("MQTT broker not running on localhost:1883. Please start an MQTT broker (e.g., Mosquitto) and try again.")
        sys.exit(1)
    
    logging.info("Starting all simulation components...")

    # Dictionary of simulation scripts to run.
    scripts = {
        "MQTT Sensor": "mqtt_sensor_simulation.py",
        "CoAP Sensor": "coap_sensor_simulation.py",
        "OPC UA Sensor": "opcua_sensor_simulation.py",
        "Data Visualization": "data_visualization.py"
    }

    processes = {}
    threads = {}

    # Launch each script as a subprocess and start a thread to log its output.
    for name, script in scripts.items():
        proc = start_process(script)
        processes[name] = proc
        thread = threading.Thread(target=log_output, args=(proc, name))
        thread.daemon = True  # Daemonize thread so it exits when the main thread does.
        thread.start()
        threads[name] = thread

    try:
        # Keep the main thread alive while the subprocesses run.
        while True:
            time.sleep(1)
            # If any process terminates unexpectedly, log a warning and exit.
            for name, proc in processes.items():
                if proc.poll() is not None:
                    logging.warning(f"{name} process terminated unexpectedly.")
                    raise SystemExit
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Terminating all processes...")
    finally:
        # Terminate all subprocesses.
        for name, proc in processes.items():
            logging.info(f"Terminating {name} process...")
            proc.terminate()
        # Ensure all output threads are joined.
        for name, thread in threads.items():
            thread.join()
        logging.info("All processes terminated. Exiting application.")

if __name__ == "__main__":
    main()
