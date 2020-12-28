host = 'dbi20.flexline.ru'
user = 'sormuser'
password = 'proxy'
db = 'lbilling19'


def sql_index(first_date, last_date):
    return f'''
               select count(day.ip), sum(day.cin)/1024/1024/1024, sum(day.cout)/1024/1024/1024, day.id
               from day where
               day.timefrom >= "{first_date}" and day.timefrom < "{last_date}" group by day.id;
               '''


def sql_ip(ip, first_date, last_date):
    return f'''
                    select 
                    v.login, v.current_shape, sum(d.cin)/1024/1024/1024, sum(d.cout)/1024/1024/1024
                    from day d
                    inner join vgroups v on (d.vg_id=v.vg_id)
                    inner join staff st on (v.vg_id=st.vg_id)
                    where
                    st.segment=inet_aton("{ip}") and
                    d.timefrom >= "{first_date}" and d.timefrom < "{last_date}";
                    '''


def sql_login(login, first_date, last_date):
    return f'''
                   select 
                   v.login, v.current_shape, sum(d.cin)/1024/1024/1024, sum(d.cout)/1024/1024/1024
                   from day d
                   inner join vgroups v on (d.vg_id=v.vg_id)
                   inner join staff st on (v.vg_id=st.vg_id)
                   where
                   v.login="{login}" and 
                   d.timefrom >= "{first_date}" and d.timefrom < "{last_date}";
                   '''
