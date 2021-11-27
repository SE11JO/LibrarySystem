# -- coding: utf-8 --
from flask import Flask, request, render_template, session, flash, redirect, url_for
import config

app = Flask(__name__)
app.secret_key = 'user_key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email'] != config.USERNAME:
            error = 'Invalid username'
            flash('Invalid username')
        elif request.form['password'] != config.PASSWORD:
            error = 'Invalid password'
            flash('Invalid password')
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('login'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    error = None
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('sign_up.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
