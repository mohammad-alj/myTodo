from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", is_logged_in=False)


app.run(debug=True)
