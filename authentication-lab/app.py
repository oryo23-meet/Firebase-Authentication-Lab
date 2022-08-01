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
  "databaseURL": "https://fir-project-e1ccb-default-rtdb.europe-west1.firebasedatabase.app",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database() 

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
			return redirect(url_for("signin.html"))
	else:
		return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user = {
			"email": request.form['email'], "password" : request.form['password'], "full_name" : request.form['full_name'],
			"user_name" : request.form['user_name'], "bio" : request.form['bio']
			}
			db.child("users").child(login_session['user']["localId"]).set(user)
			return redirect(url_for('signin'))
		except:
			error = "Authentication failed"
			return redirect(url_for("signup"))
	return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		tweet = {
		"title" : request.form['title'], "bio" : request.form['bio'] 
		}
		db.child("articles").push(tweet)
	return render_template("add_tweet.html")

@app.route('/tweets', methods=['GET', 'POST'])
def all_tweet():
	tweets = db.child("articles").get().val()

	return render_template("tweets.html", tweets= tweets)


if __name__ == '__main__':
    app.run(debug=True)