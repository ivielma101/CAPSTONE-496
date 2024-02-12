from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secure this key in a real application

users = {'admin@example.com': 'secret'}  # Example user

@app.route('/')
def home():
    # Redirect to login if user not in session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('account'))  # Direct to account if logged in

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('account'))  # Redirect if already logged in
    
    error = None
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        if users.get(user_email) == user_password:
            session['user_id'] = user_email  # Store user in session
            return redirect(url_for('account'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('account.html', user_id=session['user_id'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)