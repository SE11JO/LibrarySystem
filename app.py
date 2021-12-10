from flask import Flask, render_template, request, redirect, url_for
import controller
import json


app = Flask(__name__)

@app.route('/search', methods = ['GET', 'POST'])
def search():
    data = None
    if request.method == 'POST':
        if request.form.get('title') != None :
            Title = request.form['title']
            
            if Title != '' :
                response = controller.search_library_book(Title)
                dumps = json.dumps(response, ensure_ascii=False)
                data = json.loads(dumps)

                return render_template('search.html', data=data)

        elif request.form.get('check') != None :
            is_checked = request.form.getlist('check')
            ### id값 데이터베이스로 넘기고 수정하는것만 하면됨.

    return render_template('search.html', data=data)    


@app.route('/search/take', methods = ['GET','POST'])
def take():
    if request.method == 'POST':
        is_checked = request.form.get('check')
    return render_template('search.html')


if __name__ == '__main__':
    app.run()