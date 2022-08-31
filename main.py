from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

class users(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column("name", db.String(100))
	password = db.Column("password", db.String(100))
	email = db.Column("email", db.String(100))

	def __init__(self, name, password, email):
		self.name = name
		self.password = password
		self.email = email



@app.route("/")
def home():
	return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():

	if request.method == "POST":
		user = request.form["nm"]

		found_user = users.query.filter_by(name=user).first()
		if found_user:

			if found_user.name == user and found_user.password == request.form['pw']:
				session["user"] = user
				flash("Logged in successfully", "info")
				return redirect(url_for("user"))
			else:
				flash("Invalid password or username", "info")
				return redirect(url_for("login"))
		
		else:
			flash("Invalid password or username", "info")
			return redirect(url_for("login"))

	else:
		
		if "user" in session:
			flash("You are aldready logged in", "info")
			return redirect(url_for("user"))
		else:
			return render_template('login.html')



@app.route("/signup", methods=["GET", "POST"])
def signup():

	if request.method == "POST":
		new_user = request.form['new_nm']
		new_pass = request.form['new_pw']
		new_email = request.form['new_email']

		if new_user == "" or new_pass == "" or new_email == "":
			flash("*All feilds are required", "info")
			return redirect(url_for("signup"))
			
		
		else:
			if users.query.filter_by(name=new_user).first():
				flash("*Username aldready taken", "info")
				return redirect(url_for("signup"))
				 

			else:	
			
				session['user'] = new_user

				usr = users(new_user, "", "")
				db.session.add(usr)
				db.session.commit()
				
				found_user = users.query.filter_by(name=new_user).first()

				found_user.name = new_user
				found_user.password = new_pass
				found_user.email = new_email

				db.session.commit()
				return redirect(url_for("user"))

	else:
		return render_template("signup.html")


@app.route("/user", methods=["GET", "POST"])
def user():
	email = None

	if "user" in session:
		user = session["user"]
		found_user = users.query.filter_by(name=user).first()

		email = found_user.email
		session["email"] = email

		if request.method == "POST":
			email = request.form["email"]
			session["email"] = email
			found_user.email = email
			db.session.commit()

			flash("info saved!", "info")

		return render_template("user.html", user=user, email = email)
		
	else:
		flash("please log in to continue", "info")
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	if "user" in session:
		user = session["user"]
		flash(f"you have been logged out, {user}", "info")
	
		session.pop("user", None)
		session.pop("email", None)
		return redirect(url_for("login"))
	else:
		flash("you have to log in first", "info")
		return redirect(url_for("login"))
		

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)