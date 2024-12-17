from flask import Flask, jsonify, request, render_template
import sqlite3
import time
import os

app = Flask(__name__)

# Database file
DB_FILE = "sensor_data.db"

# Function to initialize the database
def init_db():
    if not os.path.exists(DB_FILE):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    distance INTEGER NOT NULL
                )
            ''')
            print("Database initialized.")

# Initialize the database
init_db()

@app.route('/')
def index():
    """Serve the HTML page."""
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def receive_data():
    """Receive distance data and store it in the database."""
    try:
        # Parse incoming JSON data
        data = request.get_json()

        # Validate 'distance' key exists
        if not data or "distance" not in data:
            return jsonify({"error": "Missing 'distance' key or invalid JSON"}), 400

        # Round distance to 0 decimal places
        distance = int(float(data["distance"]))
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Insert data into the database
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sensor_data (timestamp, distance) VALUES (?, ?)", (timestamp, distance))
            conn.commit()

        print(f"Stored in DB: Distance = {distance} cm at {timestamp}")
        return jsonify({"status": "success", "received_distance": distance}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route('/latest_data', methods=['GET'])
def get_latest_data():
    """Retrieve the last 10 records from the database."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, distance FROM sensor_data ORDER BY id DESC LIMIT 10")
            rows = cursor.fetchall()

        # Structure the data
        timestamps = [row[0] for row in rows]
        distances = [row[1] for row in rows]

        return jsonify({"timestamps": timestamps, "distances": distances})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
