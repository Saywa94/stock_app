from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user

from stockapp.forms import LoginForm, RegistrationForm
from stockapp.models import User, Boissons
from stockapp import app, db

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
