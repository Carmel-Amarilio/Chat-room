from flask import Flask, render_template

app = Flask(__name__)

@app.route("/<room>" , methods=["GET"])
def home(room):
    return render_template("index.html")

@app.route("/api/chat/<room>", methods=["POST"])
def  post_message(room):
    return "\n".join({"Carmel":"Carmel"}), 200

@app.route("/api/chat/<room>", methods=["GET"])
def get_chat(room):
    return "\n".join({"Max":"Max"}), 200

if __name__=="__main__":
    app.run()