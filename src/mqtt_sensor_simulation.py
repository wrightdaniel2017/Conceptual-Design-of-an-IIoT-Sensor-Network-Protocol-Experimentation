
import time
import random
import json
import paho.mqtt.client as mqtt

def simulate_sensor_data():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect("localhost", 1883)
    
    try:
        while True:
            temperature = random.uniform(20.0, 25.0)
            humidity = random.uniform(30.0, 50.0)
            
            payload = json.dumps({
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2)
            })
            
            client.publish("sensor/data", payload)
            print(f"Published - Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping simulation...")
    finally:
        client.disconnect()

if __name__ == "__main__":
    simulate_sensor_data()
