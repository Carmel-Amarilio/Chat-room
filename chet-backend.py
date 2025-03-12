from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
chats = {} 

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
    formatted_message = f"{timestamp} {username}: {message}"
    
    if room not in chats:
        chats[room] = []
    
    chats[room].append(formatted_message)
    return jsonify({"success": True}), 201

@app.route("/api/chat/<room>", methods=["GET"])
def get_chat(room):
    if room in chats:
        return "\n".join(chats[room]), 200
    else:
        return jsonify({"error": "No messages in this room"}), 404

if __name__ == "__main__":
    app.run(debug=True)