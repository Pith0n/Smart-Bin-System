import sqlite3

# Database file
DB_FILE = "sensor_data.db"

def view_data():
    """Fetch and display all rows from the sensor_data table."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sensor_data")
            rows = cursor.fetchall()

            if rows:
                print("ID | Timestamp           | Distance (cm)")
                print("-" * 30)
                for row in rows:
                    print(f"{row[0]}  | {row[1]} | {row[2]}")
            else:
                print("No data found in the database.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    view_data()
