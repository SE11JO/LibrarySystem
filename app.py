from flask import Flask, request, render_template, session, flash, redirect, url_for
import controller as dynamodb
import method as met
import json
from datetime import date

app = Flask(__name__)
app.secret_key = 'user_key'
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET', 'POST'])
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
                    session['user'] = request.form['email']

                    flash('You are logged in as {}, Welcome!'.format(response['Item']['Name']))
                    return redirect(url_for('main'))
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

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/main/manage')
def manage():
    response = met.select_all()
    json_string = json.dumps(response, ensure_ascii=False)
    json_object = json.loads(json_string)

    return render_template('manage.html', object=json_object)

@app.route('/main/manage/create')
def create():
    return render_template('create.html')

@app.route('/insert_db', methods=['POST'])
def insert_db():
    id = request.form['id']
    title = request.form['title']
    author = request.form['author']
    publish = request.form['publish']

    met.put_table(id, title, author, publish)

    return render_template('insert_db.html')

@app.route('/main/manage/update', methods=["POST", "GET"])
def update():
    title = request.form["c_title"]
    print(title)
    if title==None:
        return render_template('manage.html')

    response = met.get_book(title)
    json_string = json.dumps(response, ensure_ascii=False)
    json_object = json.loads(json_string)

    return render_template('update.html', object=json_object, title=title)

@app.route('/update_db', methods=["POST"])
def update_db():
    b_title = request.form['c_title']
    id = request.form['id']
    title = request.form['title']
    author = request.form['author']
    publish = request.form['publish']
    rental = request.form['rental']
    ren_date = request.form['ren_date']
    ren_name = request.form['ren_name']

    print(b_title)

    met.update_table(b_title, id, title, author, publish, rental, ren_date, ren_name)

    return render_template('update_db.html')

@app.route('/delete_db/<string:d_title>', methods=["GET"])
def delete_db(d_title):
    title = d_title
    print(title)
    met.delete_table(title)

    return render_template('delete_db.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    data = None
    if request.method == 'POST':
        if request.form.get('title') != None:
            Title = request.form['title']

            if Title != '':
                response = dynamodb.search_library_book(Title)
                dumps = json.dumps(response, ensure_ascii=False)
                data = json.loads(dumps)

        elif request.form.get('check') != None:
            is_checked = request.form.getlist('check')

            for i in is_checked:
                today = date.today()
                today = today.strftime("%Y-%m-%d")
                response = dynamodb.change_rental_status(i, "name", today)
            flash('대출되었습니다.')
            return render_template('search.html')

    return render_template('search.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
