from flask import Flask, render_template, request, jsonify
from datetime import datetime
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection(): #Carmel & Max
    return mysql.connector.connect(
        host='db', 
        user='root',
        password='123',
        database='chat_db'
    )


@app.route("/", methods=["GET"]) #Carmel
def home():
    return render_template("index.html")


@app.route("/<room>", methods=["GET"]) #Max
def home_room(room):
    return render_template("index.html")


@app.route("/api/chat/<room>", methods=["POST"]) #Carmel
def post_message(room):
    try:
        username = request.form.get("username")
        message = request.form.get("msg")
        
        if not username or not message:
            return jsonify({"error": "Both username and message are required."}), 400

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while saving the message."}), 500


@app.route("/api/chat/<room>", methods=["GET"]) #Max
def get_chat(room):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT timestamp, username, message FROM chats WHERE room = %s ORDER BY timestamp", (room,))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        if rows:
            formatted_messages = "\n".join(
                f"[{row['timestamp']}] {row['username']}: {row['message']}" for row in rows
            )
            return formatted_messages, 200
        else:
            return "No messages in this room", 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while retrieving messages."}), 500

#if __name__ == "__main__":
 #   app.run(debug=True, host="0.0.0.0" )


