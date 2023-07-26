from flask import Flask, render_template, request
from helpers import error

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
            return error(error_code=403, message='Username length must be between 5 and 16 characters.')

        # validate password
        password = request.form.get('password')
        num_char_freq = {
            'numbers': 0,
            'characters': 0
        }
        for c in password:
            if c.isascii():
                num_char_freq["characters"] += 1
            elif c.isdigit:
                num_char_freq['numbers'] += 1

        if num_char_freq['characters'] < 4 or num_char_freq['numbers'] < 2:
            return error(error_code=403, message='Password must atleast contain 4 characters and 2 numbers.')

        # validate password confirmation
        if password != request.form.get('confirm-password'):
            return error(error_code=403, message='Passwords do not match.')

    return render_template("register.html", is_logged_in=logged_in)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", is_logged_in=logged_in)


if __name__ == "__main__":
    app.run(debug=True)
