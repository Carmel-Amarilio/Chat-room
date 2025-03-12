from flask import Flask, render_template, request, jsonify
from datetime import datetime
import mysql.connector

app = Flask(__name__)

# MySQL connection setup
def get_db_connection():
    return mysql.connector.connect(
        host='db',  # Docker container name for MySQL service
        user='root',
        password='password',
        database='chat_db'
    )

# Create the tables in the database (to be run once at the start)
def init_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        room VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    connection.commit()
    cursor.close()
    connection.close()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/<room>", methods=["GET"])
def home_room(room):
    return render_template("index.html")

@app.route("/api/chat/<room>", methods=["POST"])
def post_message(room):
    username = request.form.get("username")
    message = request.form.get("msg")
    
    if not username or not message:
        return jsonify({"error": "Both username and message are required."}), 400

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO chats (room, username, message, timestamp) VALUES (%s, %s, %s, %s)",
        (room, username, message, timestamp)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"success": True}), 201

@app.route("/api/chat/<room>", methods=["GET"])
def get_chat(room):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT timestamp, username, message FROM chats WHERE room = %s ORDER BY timestamp", (room,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    if rows:
        formatted_messages = "\n".join(
            f"{row['timestamp']} {row['username']}: {row['message']}" for row in rows
        )
        return formatted_messages, 200
    else:
        return "No messages in this room", 200

if __name__ == "__main__":
    init_db()  # Initialize database (only needed once)
    app.run(debug=True, host="0.0.0.0")
