from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:deucalion@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Makes my class for the database
class Post(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	text = db.Column(db.String(120))

	def __init__(self, title, text):
		self.title = title 
		self.text = text

# Home page you first load into, takes the forms from 'newpost' and adds to DB
@app.route('/', methods=['GET', 'POST'])
def index():# for title 
	if request.method == 'POST':   
		text_input = request.form['text']
		title_input = request.form['title']
		# DB stuff
		title = Post(title_input,text_input)
		db.session.add(title)
		db.session.commit()
		title = Post.query.all()
		return render_template('dashboard.html', title = title, text= title)
	else:
		title = Post.query.all()
		return render_template('dashboard.html', title = title, text = title)
 
#renders submit page
@app.route('/newpost', methods=["GET", "POST"])
def submit():
	#attempt at error, gives key error for both 'title' and 'text'
	#============================================================
	#if request.method == 'POST':
	#	title_input = request.form['title']
	#	text_input = request.form['text']
	#	if title_input and text_input == '':
	#		error = 'You must submit something in BOTH fields!'
	#		return render_template('submit-page.html', error= error)
	#else:
	#	error = ''
	return render_template('submit-page.html')
	#, error= error)

#renders each blog post (Eventually)
@app.route('/blog', methods=["GET"])
def display():
	individual = request.args.get('id')
	if individual:
		thing = Post.query.get(individual)
		return render_template('blog.html', thing = thing)
	else:
		all_posts = Post.query.all()
		return render_template('dashboard.html', title = all_posts, text = all_posts )


if __name__ == '__main__':
	app.run()
	