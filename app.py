from flask import Flask, request, render_template, session
import boto3
import controller
import json

dynamodb_client = boto3.client('dynamodb', region_name = 'ap-northeast-2')

app = Flask(__name__)

@app.route('/rental', methods=['GET'])
def rental_book():
    response = controller.check_rental_possible(session['user'])

    if response['Item']['rental']:
        response = controller.change_rental_status(session['user'])
        return '대여 되었습니다'
    
    return '대여가 불가능 합니다' 

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    data = None
    response = controller.rental_search_book(session['user'])
    dumps = json.dumps(response, ensure_ascii = False)
    data = json.loads(dumps)

    if request.method == 'POST':
        list = request.form.getlist('check')
        
        for i in list:

            response = controller.return_book(i)

        response = controller.rental_search_book(session['user'])
        dumps = json.dumps(response, ensure_ascii = False)
        data = json.loads(dumps)

        return render_template('return.html', data=data)

    return render_template('return.html', data=data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)