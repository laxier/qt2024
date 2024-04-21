import warnings
import pymysql.cursors
import pandas as pd

def get_dbases():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='rootroot',
                                 charset='utf8mb4',
                                 database="newnewnwenwe",
                                 cursorclass=pymysql.cursors.Cursor)

    print('Подключение к MySQL прошло успешно')
    with connection.cursor() as cursor:
        cursor.execute("show tables")
        dbases = [i[0] for i in cursor.fetchall()]
        print(dbases)
    connection.close()

def get_table(bdname):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='rootroot',
                                 charset='utf8mb4',
                                 database="newnewnwenwe",
                                 cursorclass=pymysql.cursors.Cursor)

    print('Подключение к MySQL прошло успешно')
    with connection.cursor() as cursor:

        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{bdname}'")
        header = [i[0] for i in cursor.fetchall()]
        print(header)
        cursor.execute(f"SELECT * FROM {bdname}")
        rows = cursor.fetchall()
        print(rows)
    connection.close()

get_dbases()

get_table('testtt')