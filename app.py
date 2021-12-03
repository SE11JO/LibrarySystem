from flask import Flask, render_template, request, redirect, url_for
import controller
import json


app = Flask(__name__)

@app.route('/search', methods = ['GET', 'POST'])
def search():
    data = None
    if request.method == 'POST':
        Title = request.form['title']
        if Title != '' :
            response = controller.search_library_book(Title)
            dumps = json.dumps(response, ensure_ascii=False)
            data = json.loads(dumps)

        return render_template('search.html', data=data)

    return render_template('search.html', data=data)    


if __name__ == '__main__':
    app.run()