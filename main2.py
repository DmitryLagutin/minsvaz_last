from prettytable import from_db_cursor
import pymysql.cursors
import csv
import ipaddress
from prettytable import PrettyTable

first_date = '2020-01-01 00:00:00'
last_date = '2020-12-01 00:00:00'

main_list = []
connection = pymysql.connect(host='dbi20.flexline.ru',
                             user='sormuser',
                             password='proxy',
                             db='lbilling19',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = f'''
    select count(day.ip), sum(day.cin)/1024/1024/1024, sum(day.cout)/1024/1024/1024, day.id
    from day where
    day.timefrom >= "{first_date}" and day.timefrom < "{last_date}" group by day.id;
    '''
    list_result = []
    cursor.execute(sql)
    x = PrettyTable()
    x.field_names = ['count ip', 'in traffic (Gb)',
                     'out traffic (Gb)', 'id']

    for row in cursor:
        list_result.append([row['count(day.ip)'],
                            row['sum(day.cin)/1024/1024/1024'],
                            row['sum(day.cout)/1024/1024/1024'],
                            row['id']])
    x.add_rows(list_result)
    print(x)

    print(x.get_html_string())

