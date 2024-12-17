import time
import requests
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

# Flask server URL
FLASK_SERVER_URL = "http://192.168.0.52:5000/data"  # Replace with Flask server IP

# Sensor setup
SENSOR_PORT = 5
sensor = GroveUltrasonicRanger(SENSOR_PORT)

def send_data_to_server(distance):
    try:
        truncated_distance = int(distance)  # Truncate to no decimals
        payload = {"distance": truncated_distance}
        print(f"Sending payload: {payload}")
        response = requests.post(FLASK_SERVER_URL, json=payload)
        print(f"Server Response: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending data: {e}")

def main():
    print("Starting Ultrasonic Sensor Data Transmission...")
    while True:
        try:
            distance = sensor.get_distance()
            print(f"Measured Distance: {int(distance)} cm")  # Display truncated value
            send_data_to_server(distance)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
