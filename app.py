import re
from flask import Flask, render_template, request
from boto3.dynamodb.conditions import Key, Attr
import method as met
from pprint import pprint
import boto3
import json
from botocore.exceptions import ClientError
from flask.wrappers import Response
from werkzeug.wrappers import response
from flask import jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


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


@app.route('/list_book')
def list_book():
    response = met.select_all()
    json_string = json.dumps(response, ensure_ascii=False)
    json_object = json.loads(json_string)

    return render_template('/list_book.html', object=json_object)


@app.route('/update_db')
def update_db():
    id = request.form['id']
    title = request.form['title']
    author = request.form['author']
    publish = request.form['publish']
    rental = request.form['rental']
    ren_date = request.form['ren_date']

    suc = met.update_table(id, title, author, publish, rental, ren_date)

    return render_template('update_db.html')


if __name__ == '__main__':
    app.run()
