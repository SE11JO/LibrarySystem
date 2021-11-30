from flask import Flask, render_template, request

import boto3

app = Flask(__name__)

dynamodb_client = boto3.client('dynamodb')

table_name = 'TEST'

@app.route("/", methods=['GET', 'POST'])
def search():
    if request.method == 'POST' :
        title = request.form['title']
        
        result = read_from_Table(title)
        
    return render_template('search.html')


def read_from_Table(id):
    Table = dynamodb_client.Table('TEST')
    response = Table.get_item(
        Key={
            'id': id
        },
        AttributesToGet=[
            'name'
        ]
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)