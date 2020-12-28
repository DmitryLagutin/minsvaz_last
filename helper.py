from prettytable import from_db_cursor
from flask import Flask, request, session, redirect, url_for, render_template
import pymysql.cursors
from settings import sql_index, sql_ip, sql_login, host, user, password, db
import csv
import ipaddress
from prettytable import PrettyTable

main_list = []
connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=db,
                             cursorclass=pymysql.cursors.DictCursor)


def main_function(first_date, last_date):
    return basic_func(sql_index(first_date, last_date))


def for_ip_func(ip, first_date, last_date):
    return basic_func(sql_ip(ip, first_date, last_date))


def for_login_func(login, first_date, last_date):
    return basic_func(sql_login(login, first_date, last_date))


def basic_func(sql_str):
    connection.ping()
    try:
        with connection.cursor() as cursor:
            sql = sql_str
            list_result = []
            cursor.execute(sql)
            for row in cursor:
                list_keys = list(dict(row).keys())
                list_result.append(dict(id_0=row[list_keys[0]], id_1=row[list_keys[1]],
                                        id_2=row[list_keys[2]], id_3=row[list_keys[3]]))

            return list_result
    except Exception as ex:
        print(str(ex))
        return render_template('error.html')
    finally:
        cursor.close()
