from flask import Flask, render_template, request, jsonify
from analyzer import URLAnalyzer
import json
import os
from datetime import datetime

app = Flask(__name__)

analyzer = URLAnalyzer()
HISTORY_FILE = "history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_result(result):
    history = load_history()

    history.insert(0, result)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history[:50], file, indent=4)


@app.route("/")
def home():
    history = load_history()
    return render_template("index.html", history=history)


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "success": False,
            "message": "Please enter a URL."
        })

    result = analyzer.analyze(url)

    result["date"] = datetime.now().strftime("%d/%m/%Y %H:%M")

    save_result(result)

    return jsonify({
        "success": True,
        "result": result
    })


@app.route("/history")
def history():
    return jsonify(load_history())


if __name__ == "__main__":
    app.run(debug=True)
