from flask import Flask, render_template, request, redirect, url_for
import controller
import json


app = Flask(__name__)

@app.route('/search', methods = ['GET', 'POST'])
def home():

    return render_template('search.html')

@app.route('/result', methods = ['GET', 'POST'])
def result():
    if request.method == 'POST':
        Title = request.form['title']
        response = controller.search_library_book(Title)
        json_string = json.dumps(response, ensure_ascii=False)
        json_object = json.loads(json_string)

        return render_template('result.html', data=json_object)


if __name__ == '__main__':
    app.run()