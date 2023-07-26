from flask import Flask, render_template, request

app = Flask(__name__)

logged_in = False


@app.route("/")
def index():
    return render_template("index.html", is_logged_in=logged_in)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        # validate username
        username = request.form.get('username')
        if len(username) < 5 or len(username) > 16:
            return render_template('error.html', error_code=403, message='Username length must be between 5 and 16 characters.')

    return render_template("register.html", is_logged_in=logged_in)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", is_logged_in=logged_in)


if __name__ == "__main__":
    app.run(debug=True)
