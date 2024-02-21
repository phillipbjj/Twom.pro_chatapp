# backend.py

from flask import Flask, render_template, request
import backend  # Assuming you have a backend module with the necessary functions

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        text = request.form.get('textbox')
        # Assuming you have a function called 'twompro_chatapp' in your 'backend' module
        output = backend.twompro_chatapp(float(text))
        return render_template("index.html", output=output, user_text=text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
