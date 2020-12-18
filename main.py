from flask import Flask, request, session, redirect, url_for, render_template
from helper import main_function

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        first_date = request.form['first_date']
        last_date = request.form['last_date']
        if first_date is '' or last_date is '':
            return render_template('not_date.html')
        x = first_date.split('T')
        y = last_date.split('T')
        first_date = x[0] + ' ' + x[1] + ':00'
        last_date = y[0] + ' ' + x[1] + ':00'
        agents = main_function(first_date, last_date)
        return render_template('good_calculate.html', agents=agents)


if __name__ == "__main__":
    app.run()
