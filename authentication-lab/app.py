from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyDjkOebGjGMYjd9V7qDoKFR7Ve8QbqI8W4",
  "authDomain": "fir-project-e1ccb.firebaseapp.com",
  "projectId": "fir-project-e1ccb",
  "storageBucket": "fir-project-e1ccb.appspot.com",
  "messagingSenderId": "928680021126",
  "appId": "1:928680021126:web:74cc478ef89e7683519507",
  "measurementId": "G-SK8WTZ2LWS",
  "databaseURL": "",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
			return render_template("signup.html")	
	return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)