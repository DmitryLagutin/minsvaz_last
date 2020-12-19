from prettytable import from_db_cursor
import pymysql.cursors
import csv
import ipaddress
from prettytable import PrettyTable

ip = '195.28.60.29'
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
    select 
    v.login, v.current_shape, sum(d.cin)/1024/1024/1024, sum(d.cout)/1024/1024/1024
    from day d
    inner join vgroups v on (d.vg_id=v.vg_id)
    inner join staff st on (v.vg_id=st.vg_id)
    where
    st.segment=inet_aton("{ip}") and
    d.timefrom >= "{first_date}" and d.timefrom < "{last_date}";
    '''

    list_result = []
    x = PrettyTable()
    x.field_names = ['login', 'current shape',
                     'in traffic (Gb)', 'out traffic (Gb)']

    cursor.execute(sql)

    for row in cursor:
        print(row)
        list_result.append([row['login'],
                            row['current_shape'],
                            row['sum(d.cin)/1024/1024/1024'],
                            row['sum(d.cout)/1024/1024/1024']])
    x.add_rows(list_result)
    print(f'Результат для ip - адреса {ip}')
    print(x)

    print(x.get_html_string())
