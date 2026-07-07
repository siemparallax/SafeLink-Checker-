from flask import Flask, render_template, request, jsonify
from analyzer import URLAnalyzer
import json
import os
from datetime import datetime


app = Flask(__name__)

analyzer = URLAnalyzer()

HISTORY_FILE = "history.json"


def get_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_history(data):
    history = get_history()

    history.insert(0, data)

    history = history[:20]

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


@app.route("/")
def index():
    history = get_history()

    return render_template(
        "index.html",
        history=history
    )


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    url = data.get("url")

    if not url:
        return jsonify({
            "error": "URL cannot be empty"
        })


    result = analyzer.analyze(url)

    result["checked_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    save_history(result)


    return jsonify(result)



@app.route("/history")
def history():

    return jsonify(get_history())



if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
