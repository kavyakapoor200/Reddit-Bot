from flask import Flask, render_template, request
from bot_logic import generate_from_strategy, post_to_subreddit
from fallback_runner import start_fallback, stop_fallback

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/choose")
def choose():
    return render_template("choose_mode.html")

@app.route("/strategy", methods=["GET", "POST"])
def strategy():
    output = ""
    if request.method == "POST":
        strategy = request.form.get("strategy")
        sr, title, body = generate_from_strategy(strategy)
        msg = post_to_subreddit(sr, title, body, force=True)
        output = f"Posted to {sr}<br><b>{title}</b><br>{body}"
    return render_template("strategy.html", output=output)

@app.route("/fallback", methods=["GET", "POST"])
def fallback():
    if request.method == "POST":
        start_fallback()
        return render_template("fallback.html", message="Fallback posting started!")
    return render_template("fallback.html", message="")
if __name__ == "__main__":
    print("Server starting on http://127.0.0.1:5000 ...")
    app.run(debug=True)
