from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import date
import controller
import json


app = Flask(__name__)
app.secret_key = '1234'

@app.route('/main/search', methods = ['GET', 'POST'])
def search():
    data = None
    if request.method == 'POST':
        if request.form.get('title') != None :
            Title = request.form['title']
            
            if Title != '' :
                response = controller.search_library_book(Title)
                dumps = json.dumps(response, ensure_ascii=False)
                data = json.loads(dumps)

        elif request.form.get('check') != None :
            is_checked = request.form.getlist('check')

            for i in is_checked:
                today = date.today()
                today = today.strftime("%Y-%m-%d") 
                response = controller.change_rental_status(i, "name", today)
            flash('대출되었습니다.')
            return render_template('search.html')    



    return render_template('search.html', data=data)    


if __name__ == '__main__':
    app.run()
