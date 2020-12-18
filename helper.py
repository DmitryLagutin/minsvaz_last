from prettytable import from_db_cursor
import pymysql.cursors
import csv
import ipaddress
from prettytable import PrettyTable


main_list = []
connection = pymysql.connect(host='dbi20.flexline.ru',
                             user='sormuser',
                             password='proxy',
                             db='lbilling19',
                             cursorclass=pymysql.cursors.DictCursor)


def main_function(first_date, last_date):
    with connection.cursor() as cursor:
        sql = f'''
        select count(day.ip), sum(day.cin)/1024/1024/1024, sum(day.cout)/1024/1024/1024, day.id
        from day where
        day.timefrom >= "{first_date}" and day.timefrom < "{last_date}" group by day.id;
        '''
        list_result = []
        cursor.execute(sql)
        # x = PrettyTable()
        # x.field_names = ['count ip', 'in traffic (Gb)',
        #                  'out traffic (Gb)', 'id']
        for row in cursor:
            list_result.append(dict(count_ip=row['count(day.ip)'], sum_in=row['sum(day.cin)/1024/1024/1024'],
                                    sum_out=row['sum(day.cout)/1024/1024/1024'], id=row['id']))

        return list_result
