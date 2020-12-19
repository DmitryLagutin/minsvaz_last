from flask import Flask, request, session, redirect, url_for, render_template
import pymysql.cursors
from helper import main_function, for_ip_func, for_login_func

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        first_date = request.form['first_date']
        last_date = request.form['last_date']
        print(first_date, last_date)
        if first_date is '' or last_date is '':
            return render_template('not_date.html')
        first_date = first_date + ' ' + '00:00:00'
        last_date = last_date + ' ' + '00:00:00'
        agents = main_function(first_date, last_date)
        return render_template('good_calculate.html', agents=agents)


@app.route("/for_ip", methods=['GET', 'POST'])
def for_ip():
    if request.method == 'GET':
        return render_template('for_ip.html')
    elif request.method == 'POST':
        ip = request.form['ip']
        first_date = request.form['first_date']
        last_date = request.form['last_date']
        print(first_date, last_date, ip)
        if first_date is '' or last_date is '' or ip is '':
            return render_template('not_date.html')
        first_date = first_date + ' ' + '00:00:00'
        last_date = last_date + ' ' + '00:00:00'
        rows = for_ip_func(ip, first_date, last_date)
        return render_template('good_calc_ip.html', rows=rows, ip=ip)


@app.route("/for_login", methods=['GET', 'POST'])
def for_login():
    if request.method == 'GET':
        return render_template('for_login.html')
    elif request.method == 'POST':
        login = request.form['login']
        first_date = request.form['first_date']
        last_date = request.form['last_date']
        print(first_date, last_date, login)
        if first_date is '' or last_date is '' or login is '':
            return render_template('not_date.html')
        first_date = first_date + ' ' + '00:00:00'
        last_date = last_date + ' ' + '00:00:00'
        rows = for_login_func(login, first_date, last_date)
        return render_template('good_calc_login.html', rows=rows, login=login)


if __name__ == "__main__":
    app.run()
