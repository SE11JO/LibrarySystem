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
def main():
    return render_template('main.html')

@app.route('/manage')
def manage():
    response = met.select_all()
    json_string = json.dumps(response, ensure_ascii=False)
    json_object = json.loads(json_string)

    return render_template('manage.html', object=json_object)

@app.route('/manage/create')
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

@app.route('/manage/update', methods=["POST", "GET"])
def update():
    id = request.form.get['c_id']
    print(id)
    if id==None:
        return render_template('manage.html')

    response = met.get_book(id)
    json_string = json.dumps(response, ensure_ascii=False)
    json_object = json.loads(json_string)

    return render_template('update.html', object=json_object)

@app.route('/update_db')
def update_db():
    id = request.form['id']
    title = request.form['title']
    author = request.form['author']
    publish = request.form['publish']
    rental = request.form['rental']
    ren_date = request.form['ren_date']
    ren_name = request.form['ren_name']

    met.update_table(id, title, author, publish, rental, ren_date, ren_name)

    return render_template('update_db.html')

@app.route('/manage/delete', methods=["GET"])
def delete_db():
    id = request.form['c_title']
    print(id)
    met.delete_table(id)

    return render_template('delete_db.html')

if __name__ == '__main__':
    app.run()
