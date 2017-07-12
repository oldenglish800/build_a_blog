from flask import Flask, request, redirect, render_template
import cgi
import re

app = Flask(__name__)

app.config['DEBUG'] = True

def is_invalid(text):
    return re.search(r"\s+", text) or re.search(r"^.{0,2}$", text) or re.search(r"^.{20,}$", text)


@app.route("/", methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    verifypassword = request.form['verifypassword']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verfiy_error = ''
    email_error = ''

    if is_invalid(username):
        username_error = "That's not a valid username"
    if is_invalid(password):
        password_error = "That's not a valid password"
    if verifypassword == '':
        verfiy_error = "That's not a valid password"
    if verifypassword != password:
        verfiy_error = "Passwords don't match"
    if email != '' and (email.count("@") != 1 or email.count(".") != 1 or is_invalid(email)):
        email_error = "That's not a valid email"


    if not (username_error or password_error or verfiy_error or email_error):
        return redirect('/welcome?username=' + username)
    else:
        return render_template('signin.html',
            username = username,
            email = email,
            username_error = username_error,
            password_error = password_error,
            verfiy_error = verfiy_error,
            email_error = email_error)


@app.route("/welcome")
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)


@app.route("/")
def index():
    return render_template('signin.html')

app.run ()