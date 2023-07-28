from flask import render_template, session, redirect


def error(error_code, message):
    return render_template('error.html', error_code=error_code, message=message)


def login_required(f):
    def wrapper(*args, **kwargs):
        if not session['user_id']:
            return redirect('/login')
        f(*args, **kwargs)
    return wrapper
