from flask import Flask, render_template, request, session, redirect
from helpers import error, login_required, validate_username, validate_password
from keys import SECRET_KEY
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

logged_in = False

db = SQL('sqlite:///database.db')


@app.route("/")
def index():
    if 'user_id' in session:
        lists = db.execute(
            'SELECT * FROM lists WHERE user_id = ?', session['user_id'])
        return render_template("index.html", lists=lists)
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        # validate username
        username = request.form.get('username')
        usr_validation = validate_username(username)
        if not usr_validation['success']:
            return error(403, usr_validation['error_message'])

        # validate password
        password = request.form.get('password')
        pwd_validation = validate_password(password)
        if not pwd_validation['success']:
            return error(403, pwd_validation['error_message'])

        # validate password confirmation
        if password != request.form.get('confirm-password'):
            return error(error_code=403, message='Passwords do not match.')

        # all good now

        # add user to the database
        user_id = db.execute(
            'INSERT INTO users (username, hash) VALUES (?, ?)', username, generate_password_hash(password))

        # add session
        session['user_id'] = user_id
        session['password'] = password

        # tell that the user is registerd
        return render_template('success.html', title='Acount created', heading='Your acount has been created!')

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # check if user in database

        # check the username
        rows = db.execute('SELECT * FROM users WHERE username = ?',
                          username)
        user = None if not rows else rows[0]

        if not user:
            return error(403, 'User does not exist.')

        # check the password
        if not check_password_hash(pwhash=user['hash'], password=password):
            return error(403, 'Invalid password.')

        # all done
        session['user_id'] = user['user_id']
        session['password'] = password
        return render_template('success.html', heading='You have logged in!', title='logged in')
    return render_template("login.html")


@app.route('/acount')
@login_required
def acount():
    user = db.execute('SELECT * FROM users WHERE user_id = ?',
                      session['user_id'])[0]

    return render_template('acount.html', username=user['username'], password=session['password'])


@app.route('/acount/change-username', methods=['POST'])
def change_username():
    username = request.form.get('username')
    usrnm_validation = validate_username(username)
    if not usrnm_validation['success']:
        return error(403, usrnm_validation['error_message'])

    # change username in database
    db.execute('UPDATE users SET username = ? WHERE user_id = ?',
               username, session['user_id'])

    return render_template('success.html', heading='Username updated!')


@app.route('/acount/change-password', methods=['POST'])
def change_password():
    password = request.form.get('password')
    pw_validation = validate_password(password)
    if not pw_validation['success']:
        return error(403, pw_validation['error_message'])

    confirm_password = request.form.get('confirm-password')
    if password != confirm_password:
        return error(403, 'Passwords don\'t match!')

    # change hash in database
    db.execute('UPDATE users SET hash = ? WHERE user_id = ?',
               generate_password_hash(password), session['user_id'])

    session['password'] = password
    return render_template('success.html', heading='Password updated!')


@app.route('/acount/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/lists', methods=['POST'])
def lists():
    if request.method == 'POST':
        list_name = request.form.get('list-name')
        if not list_name:
            return error(403, 'you must provide a name for the list.')
        list_id = db.execute('INSERT INTO lists (user_id, list_name) VALUES (?, ?)',
                             session['user_id'], list_name)
        return redirect(f'/lists/{list_id}')


@app.route('/lists/<list_id>', methods=['GET', 'POST'])
def list(list_id):
    if request.method == 'GET':
        list = db.execute(
            'SELECT * FROM lists WHERE user_id = ? AND list_id = ?', session['user_id'], list_id)
        if not list:
            return error(403, 'you dont have that list')
        list = list[0]

        tasks = db.execute('SELECT * FROM tasks WHERE list_id = ?', list_id)
        return render_template('list.html', list=list, tasks=tasks)
    elif request.method == 'POST':

        task_content = request.form.get('task')
        if not task_content:
            return error('you must provide a task.')
        db.execute(
            'INSERT INTO tasks (list_id, task_content) VALUES (?, ?)', list_id, task_content)
        return redirect(f'/lists/{list_id}')


@app.route('/lists/<list_id>/remove_task/<task_id>', methods=['POST'])
def remove_task(list_id, task_id):
    db.execute(
        'DELETE FROM tasks WHERE task_id = ? AND list_id = ?', task_id, list_id)
    return redirect(f'/lists/{list_id}')


@app.route('/lists/remove-list/<list_id>', methods=['POST'])
def remove_list(list_id):
    db.execute('DELETE FROM lists WHERE list_id = ? AND user_id = ?',
               list_id, session['user_id'])
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
