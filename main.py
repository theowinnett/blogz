from flask import  Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:deucalion@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y33tiyghjgkcjg'

# How to password check?

# Makes my class for the databases
class Post(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	text = db.Column(db.String(120))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, title, text, owner):
		self.title = title 
		self.text = text
		self.owner = owner
													#classes (models)
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(120))
	password = db.Column(db.String(120))
	blogs = db.relationship('Post', backref='owner')

	def __init__(self, username, password):
		self.username = username 
		self.password = password

@app.before_request
def require_login():
	allowed_routes = ['login', 'signup','blog']
	if request.endpoint not in allowed_routes and 'username' not in session:
		flash("Login!")
	else:
		redirect('/')
	
#handlers (controlers)

@app.route('/', methods=['GET', 'POST'])
def index():
	post_db = Post.query.all()
	users = User.query.all()
	return render_template('dashboard.html', post_db = post_db, users = users)

#renders individual blogs

@app.route('/blog', methods=["GET"])
def display():
	individual = request.args.get('id')
	individual_user = request.args.get('user')
	users = User.query.all()
	if individual:
		post_db = Post.query.filter_by(id = individual)
		return render_template('blog.html', post_db = post_db, users = users)
	elif individual_user:
		post_db = Post.query.filter_by(user_id = individual_user)
		return render_template('blog.html', post_db = post_db, users = users)
	else:
		post_db = Post.query.all()
		return render_template('blog.html', post_db = post_db, users = users)

#renders submit page

@app.route('/newpost', methods=["GET", "POST"])
def submit():
	if 'username' in session:
		if request.method == 'POST':		
			owner = User.query.filter_by(username=session['username']).first()
			text_input = request.form['text']
			title_input = request.form['title']
			# Blog stuff
			title = Post(title_input,text_input,owner)
			db.session.add(title)
			db.session.commit()
			return redirect('/blog')
		else:
			return render_template('submit-page.html')
	else:
		return redirect('/login')

#renders signup page (NEW HANDLERS BEGIN)

@app.route('/signup', methods=["GET", "POST"])
def signup():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		verify = request.form['verify']
		existing_user = User.query.filter_by(username=username).first()
		if not existing_user:
			username = request.form['username']
			password = request.form['password']
			verify = request.form['verify']
			new_user = User(username, password)
			db.session.add(new_user)
			db.session.commit()
			session['username'] = username
			return redirect('/')
		else:
			flash("Duplicate User", "error")
			return render_template('signup.html')
	else:
		return render_template('signup.html')

#renders login

@app.route('/login', methods= ["GET", "POST"])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username).first()
		if user and user.password == password:
			session['username'] = username
			flash("Logged in")
			return redirect('/')
		else:
			flash("User password incorrect, or user does not exist", "error")		
			return render_template('login.html')
	else:
		return render_template('login.html')

#performs logout

@app.route('/logout')
def logout():
		del session['username']
		return redirect('/')




if __name__ == '__main__':
	app.run()
	