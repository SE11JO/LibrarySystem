# -- coding: utf-8 --
from flask import Flask, request, render_template, session, flash, redirect, url_for
import config
import controller as dynamodb

app = Flask(__name__)
app.secret_key = 'user_key'


@app.route('/')
def index():
    dynamodb.create_table_user()
    return 'Table Created!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        response = dynamodb.read_user_information(request.form['email'])
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Item' in response:
                if request.form['email'] != response['Item']['Email']:
                    error = 'Invalid username'
                    flash('Invalid username')
                elif request.form['password'] != response['Item']['Password']:
                    error = 'Invalid password'
                    flash('Invalid password')
                else:
                    session['logged_in'] = True
                    flash('You are logged in as {}, Welcome!'.format(response['Item']['Name']))
                    return redirect(url_for('login'))
            else:
                flash('There is no such user! Please Sign Up First!')
                redirect(url_for('login'))
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
        response = dynamodb.register_new_user(request.form['email'], request.form['name'], request.form['password'])
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return redirect(url_for('login'))
        return {
            'msg': 'Some error occcured',
            'response': response
        }
    return render_template('sign_up.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
