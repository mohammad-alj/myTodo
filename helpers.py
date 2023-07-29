from flask import render_template, session, redirect, request
from cs50 import SQL

db = SQL('sqlite:///database.db')


def error(error_code, message):
    return render_template('error.html', error_code=error_code, message=message)


def login_required(f):
    def wrapper_func(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        return redirect('/login')
    return wrapper_func


def validate_username(username):
    output = {
        'error_message': ''
    }

    if len(username) < 5 or len(username) > 16:
        output['error_message'] = 'Username length must be between 5 and 16 characters.'

    # check if username already exists
    user = db.execute(
        'SELECT * FROM users WHERE username = ?', username)
    if user:
        output['error_message'] = 'Username already exists.'

    output['success'] = False if output['error_message'] else True
    return output


def validate_password(pw):
    output = {
        'error_message': ''
    }

    num_char_freq = dict(numbers=0, characters=0)
    for c in pw:
        if c.isalpha():
            num_char_freq["characters"] += 1
        elif c.isdigit():
            num_char_freq['numbers'] += 1

    print(num_char_freq)
    if num_char_freq['characters'] < 4 or num_char_freq['numbers'] < 2:
        output['error_message'] = 'Password must atleast contain 4 characters and 2 numbers.'

    output['success'] = False if output['error_message'] else True
    return output
