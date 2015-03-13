from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
     login_required
from app import app, db, login_manager
from .forms import LoginForm, RegistrationForm
from .models import User

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #user = User.query.filter_by(email=form.username.data).first()
        uname = form.username.data.split('@')[0]
        user = User(username=uname ,email=form.username.data, passwd=form.passwd.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(id):
    #return User.query.get(int(id))
    return id
@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Rk'}  # fake user
    #user = g.user
    return render_template('index.html', 
                          title='Home', user=user) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    #if g.user is not None and g.user.is_authenticated():
    #    return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.username is None or form.username == "":
            flash('Invalid login. Please try again.')
            return redirect(url_for('login'))
        if form.passwd is None or form.passwd == "":
            flash('Invalid Password. Please try again.')
            return redirect(url_for('login'))
        #user = User.query.filter_by(email=form.username.data).first()
        user = User(id=101, username='rahulk', email='rahulk@gmail.com', passwd='xyz')
        if user.email == form.username.data and user.passwd == form.passwd.data:
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', 
                           title='Sign In',
                           form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

