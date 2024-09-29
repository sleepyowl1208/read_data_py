from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import psycopg2  # Using psycopg2-binary

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
DB_CONFIG = {
    'dbname': 'HRManagementDB',
    'user': 'postgres',      # Replace with your PostgreSQL username
    'password': '12345',  # Replace with your PostgreSQL password
    'host': 'localhost',
    'port': '5433'
}


def get_db_connection():
    """Establish a database connection and return the connection object."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


@app.route('/api/users', methods=['GET'])
def get_users():
    """Fetch users from the database and return them as JSON."""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users")
        rows = cursor.fetchall()

        # Convert fetched data to a list of dictionaries
        users = [{'id': row[0], 'username': row[1], 'email': row[2]}
                 for row in rows]

        cursor.close()
        conn.close()

        return jsonify(users)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500


if __name__ == '__main__':
    app.run(debug=True)
