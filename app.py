from flask import Flask, request, render_template
import boto3
import controller
import json

dynamodb_client = boto3.client('dynamodb', region_name = 'ap-northeast-2')

app = Flask(__name__)

@app.route('/rental/', methods=["GET"])
def rental():
    response = controller.check_rental_possible(request.args["id"])

    if response['Item']['rental']:
        response = controller.change_rental_status('1')
        return '대여 되었습니다'
    
    return '대여가 불가능 합니다'


@app.route('/')
def home():
    response = controller.return_book('1')
    return 'hello'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)