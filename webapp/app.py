from flask import Flask, render_template, request, jsonify, session
import subprocess
import os
import time
import db

app = Flask(__name__)
app.secret_key = "change_this_before_you_submit" 

ENGINE_PATH = os.path.join(os.path.dirname(__file__), "..", "engine_move")

def blank_board():
    return "_________"


@app.route("/")
def home_page():
    #new game on page load
    session["board"] = blank_board()
    session["status"] = "CONTINUE"
    session["game_started_at"] = time.time()
    return render_template("index.html")


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"ok": False, "error": "username and password are required"}), 400

    try:
        user_id = db.create_user(username, password)
    except Exception:
        return jsonify({"ok": False, "error": "that username is already taken"}), 400

    session["user_id"] = user_id
    session["username"] = username
    return jsonify({"ok": True, "username": username})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    user_id = db.check_login(username, password)
    if user_id is None:
        return jsonify({"ok": False, "error": "wrong username or password"}), 401

    session["user_id"] = user_id
    session["username"] = username
    return jsonify({"ok": True, "username": username})


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return jsonify({"ok": True})


@app.route("/stats")
def stats():
    if "user_id" not in session:
        return jsonify({"error": "not logged in"}), 401
    return jsonify(db.get_stats_for_user(session["user_id"]))


@app.route("/move", methods=["POST"])
def make_move():
    data = request.get_json()
    spot = data.get("spot")

    current_board = session.get("board", blank_board())

    result = subprocess.run(
        [ENGINE_PATH, current_board, str(spot)],
        capture_output=True,
        text=True
    )

    output_line = result.stdout.strip()
    new_board, status = output_line.split("|")

    session["board"] = new_board
    session["status"] = status

    if status in ("O_WINS", "X_WINS", "DRAW") and "user_id" in session:
        started_at = session.get("game_started_at", time.time())
        seconds_taken = int(time.time() - started_at)
        result_word = "WIN" if status == "O_WINS" else "LOSS" if status == "X_WINS" else "DRAW"
        db.record_game(session["user_id"], result_word, seconds_taken)

    return jsonify({
        "board": new_board,
        "status": status
    })


@app.route("/new_game", methods=["POST"])
def new_game():
    session["board"] = blank_board()
    session["status"] = "CONTINUE"
    session["game_started_at"] = time.time()
    return jsonify({"board": session["board"], "status": session["status"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)