import mysql.connector
import datetime

connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='admin',
    password='estacionar123',
    database='estacionar-db'
)
