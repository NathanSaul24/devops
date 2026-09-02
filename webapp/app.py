from flask import Flask, render_template, request, jsonify, session
import subprocess
import os

app = Flask(__name__)
app.secret_key = "jfhbahfboSHVBFOQAwehbfo"  

ENGINE_PATH = os.path.join(os.path.dirname(__file__), "..", "engine_move")

def blank_board():
    return "_________"


@app.route("/")
def home_page():
    # new gamer on page load
    session["board"] = blank_board()
    session["status"] = "CONTINUE"
    return render_template("index.html")


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

    return jsonify({
        "board": new_board,
        "status": status
    })


@app.route("/new_game", methods=["POST"])
def new_game():
    session["board"] = blank_board()
    session["status"] = "CONTINUE"
    return jsonify({"board": session["board"], "status": session["status"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)