# FlexLine-N Traffic Monitor (minsvaz_last)

Flask-приложение для мониторинга интернет-трафика через систему FlexLine-N.

## Описание проекта

Веб-приложение для просмотра и анализа трафика абонентов системы **FlexLine-N**.

### Ключевые возможности:

✅ По monthly traffic - общий трафик по периоду  
✅ По IP-адресу - детализация трафика конкретного IP  
✅ По логину - поиск статистики по имени пользователя  
✅ Мониторинг пропускной способности сети  
✅ Отчетность для billing системы  

## Технологии

| Компонент | Описание |
|-----------|----------|
| **Язык** | Python 3.x |
| **Framework** | Flask |
| **База данных** | MySQL/PyMySQL (lbilling19) |
| **Сервер** | dbi20.flexline.ru |
| **Шаблоны** | Jinja2 HTML templates |

## Установка

### Требования

- Python 3.6+
- Библиотеки: flask, pymysql, prettytable

```bash
pip install flask pymysql prettytable
```

### Конфигурация

Редактируйте `settings.py`:

```python
host = 'dbi20.flexline.ru'
user = 'sormuser'
password = 'proxy'
db = 'lbilling19'
```

⚠️ **ВАЖНО**: Не храните credentials в открытом виде!

## Структура проекта

```
minsvaz_last/
├── main.py                   # Flask приложение
├── helper.py                 # Вспомогательные функции
├── settings.py               # Настройки подключения
└── templates/                # HTML шаблоны
    ├── index.html            # Главная страница
    ├── for_ip.html           # Поиск по IP
    ├── for_login.html        # Поиск по логину
    └── ...
```

## Использование

### Запуск приложения

```bash
python main.py
```

Откройте http://localhost:5000

### Основные endpoints

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/` | GET/POST | Главный экран |
| `/for_ip` | GET/POST | Поиск по IP-адресу |
| `/for_login` | GET/POST | Поиск по логину |

### API вызовы

```python
import requests

# Общий отчет
requests.post('http://localhost:5000/', {
    'first_date': '2024-01-01',
    'last_date': '2024-01-31'
})

# По IP
requests.post('http://localhost:5000/for_ip', {
    'ip': '192.168.1.1',
    'first_date': '2024-01-01',
    'last_date': '2024-01-31'
})
```

## SQL запросы

### Обобщенный отчет

```sql
SELECT count(day.ip), sum(cin)/GB, sum(cout)/GB, day.id
FROM day WHERE timefrom BETWEEN date1 AND date2
GROUP BY day.id
```

### Фильтр по IP

```sql
SELECT v.login, v.current_shape, sum(cin)/GB, sum(cout)/GB
FROM day d JOIN vgroups v ON d.vg_id=v.vg_id
JOIN staff st ON v.vg_id=st.vg_id
WHERE st.segment = INET_ATON(ip)
```

## Расширение функциональности

### Экспорт в CSV

```python
def export_to_csv(rows, filename):
    import csv
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Count', 'In_GB', 'Out_GB'])
        for row in rows:
            writer.writerow([row['id_0'], row['id_1'], row['id_2'], row['id_3']])
```

### Email уведомления

```python
import smtplib
from email.mime.text import MIMEText

def send_report(subject, body, recipients):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'admin@flexline.ru'
    msg['To'] = ', '.join(recipients)
    server = smtplib.SMTP('smtp.flexline.ru', 587)
    server.send_message(msg)
    server.quit()
```

## Важные предупреждения

### Безопасность

1. **Используйте .env файл для credentials!**
2. **SQL injection защита:** используйте параметризованные запросы
3. **HTTPS для продакшена!** Используйте Nginx с SSL

### Производительность

- Используйте максимум 1 месяц в запросе
- Добавьте индексы: `timefrom`, `ip`, `vg_id`

## Решенные проблемы

### Медленные запросы

```sql
CREATE INDEX idx_timefrom ON day(timefrom);
CREATE INDEX idx_vg_id ON day(vg_id);
CREATE INDEX idx_ip ON day(ip);
```

### Authentication errors

```sql
GRANT SELECT ON lbilling19.day TO 'sormuser'@'%';
GRANT SELECT ON lbilling19.vgroups TO 'sormuser'@'%';
GRANT SELECT ON lbilling19.staff TO 'sormuser'@'%';
```

## Полезные ссылки

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
- [FlexLine-N Systems](https://flexline.ru/)

## License

Внутреннее использование FlexLine-N.

## Author

Разработано [@DmitryLagutin](https://github.com/DmitryLagutin)

---

*Monitor your network efficiently!*
