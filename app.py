# This is the main py file in this app
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
import os

from werkzeug.security import generate_password_hash, check_password_hash


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login= LoginManager(app)
login.login_view = 'login'

#### To be able to drop tables from sqlalchemy
# thanks to render_as_batch function
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


########### Forms ###########################

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')



############ Declaring Models ###############
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    items = db.relationship('Boissons', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"{self.id} <{self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Boissons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(60))
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.item}, {self.quantity}"


############ Login User loader Function #####
# gives Flask_login the current_user  variable
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


############ Declaring Routes ###############
@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/configure')
@login_required
def show_table():
    u = User.query.get(current_user.id)
    all = u.items.all()
    return render_template('table.html', all=all)


@app.route('/drinks')
@login_required
def drinks():
    u = User.query.get(current_user.id)
    all = u.items.all()
    drinks_list = []
    for i in all:
        drinks_list.append(i.item)
    return render_template('drinks.html', drinks_list = drinks_list)


@app.route('/compare', methods=['POST'])
def compare():
    u = User.query.get(current_user.id)
    all = u.items.all()
    newall = []
    for i in all:
        newall.append(f"{i.item} : {i.quantity - int(request.form[i.item])}")
        # print(request.form[i.id])
    return render_template('list.html', newall=newall)



@app.route('/add', methods=['POST'])
def add():
    u = User.query.get(current_user.id)
    row = Boissons(item = request.form['drink'], quantity = request.form['how_many'], author=u)
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('show_table'))

@app.route('/delete', methods=['POST'])
def delete():
    u = User.query.get(current_user.id)
    elems = Boissons.query.filter_by(item = request.form['item'], author=u).delete()
    db.session.commit()
    return redirect(url_for('show_table'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
