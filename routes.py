from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")

@main.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            new_user = User(username=request.form['username'], password=request.form['password'])
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')

@main.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            session['logged_in'] = True
            return redirect(url_for('main.index'))
        return render_template('index.html', message="Incorrect Details")

@main.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('main.index'))
