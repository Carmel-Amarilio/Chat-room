from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
chats = {} 

@app.route("/", methods=["GET"]) #Carmel
def home():
    return render_template("index.html")

@app.route("/<room>", methods=["GET"]) #Max
def home_room(room):
    return render_template("index.html")

@app.route("/api/chat/<room>", methods=["POST"]) #Carmel
def post_message(room):
    username = request.form.get("username")
    message = request.form.get("msg")
    
    if not username or not message:
        return jsonify({"error": "Both username and message are required."}), 400
    
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    msg_data = {"timestamp": timestamp, "username": username, "message": message}
    
    if room not in chats:
        chats[room] = []
    
    chats[room].append(msg_data)
    return jsonify({"success": True}), 201

@app.route("/api/chat/<room>", methods=["GET"]) #Max
def get_chat(room):
    if room in chats:
        formatted_messages = "\n".join(
            f"{msg['timestamp']} {msg['username']}: {msg['message']}" for msg in chats[room]
        )
        return formatted_messages, 200
    else:
        return "No messages in this room", 201

if __name__ == "__main__":
    app.run(debug=True)

