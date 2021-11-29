from flask import Flask, render_template, request
from boto3.dynamodb.conditions import Key, Attr
import method as met

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/manage')
def manage():
    return render_template('manage.html')


@app.route('/create_book')
def create_book():
    return render_template('create_book.html')


@app.route('/insert_db', methods=['POST'])
def insert_db():
    id = request.form['id']
    title = request.form['title']
    author = request.form['author']
    publish = request.form['publish']

    suc = met.put_table(id, title, author, publish)

    return render_template('insert_db.html')

@app.route('/update_book')
def update():

    
    return met.select_all('library')

if __name__ == '__main__':
    app.run()
