from flask import render_template


def error(error_code, message):
    return render_template('error.html', error_code=error_code, message=message)
