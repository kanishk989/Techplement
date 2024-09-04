from flask import Flask, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from models import db, User
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

@app.before_request
def create_tables():
  db.create_all()

@app.route('/')
def start():
  render_template('base.html', )
  return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = generate_password_hash(form.password.data, method='scrypt')
    new_user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, contact=form.contact.data, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash('Account created successfully!', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if 'user_id' in session:
    flash('Already Logged in!', 'info')
    return redirect(url_for('profile'))
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and check_password_hash(user.password, form.password.data):
      session['user_id'] = user.id
      flash('Login successful!', 'success')
      return redirect(url_for('profile'))
    else:
      flash('Login unsuccessful. Please check your credentials.', 'danger')
  return render_template('login.html', form=form)

@app.route('/profile')
def profile():
  if 'user_id' not in session:
    flash('Please log in to access this page.', 'warning')
    return redirect(url_for('login'))
  user = User.query.get(session['user_id'])
  return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
  session.pop('user_id', None)
  flash('You have been logged out.', 'info')
  return redirect(url_for('login'))

if __name__ == '__main__':
  app.run(debug=True)