from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

import pymysql.cursors
import pandas as pd

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
def on_combobox_changed():
    dbname = form.selectDB.currentText()
    form.selectTable.clear()
    form.selectTable.addItems(get_tables(dbname))
def update_now():
    dbname = form.selectDB.currentText()
    tname = form.selectTable.currentText()
    model = TableModel(update_table(dbname, tname))
    form.table.setModel(model)
def update_table(bdname,tname):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='rootroot',
                                 charset='utf8mb4',
                                 database=bdname,
                                 cursorclass=pymysql.cursors.Cursor)

    # print('Подключение к MySQL прошло успешно')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tname}'")
        header = [i[0] for i in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM {tname}")
        df = pd.DataFrame(cursor.fetchall(), columns=header)
    connection.close()
    return df
def get_dbases():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='rootroot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.Cursor)

    # print('Подключение к MySQL прошло успешно')
    with connection.cursor() as cursor:
        cursor.execute("show databases")
        dbases = [i[0] for i in cursor.fetchall()]
    connection.close()
    return dbases
def get_tables(dbname):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='rootroot',
                                 charset='utf8mb4',
                                 database=dbname,
                                 cursorclass=pymysql.cursors.Cursor)

    # print('Подключение к MySQL прошло успешно')
    with connection.cursor() as cursor:
        cursor.execute("show tables")
        tables = [i[0] for i in cursor.fetchall()]
    connection.close()
    return tables

if __name__ == "__main__":
    Form, Window = uic.loadUiType("untitled.ui")

    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)

    form.selectDB.addItems(get_dbases())
    dbname = form.selectDB.currentText()
    form.selectTable.addItems(get_tables(dbname))

    form.selectDB.currentTextChanged.connect(on_combobox_changed)
    form.updater.clicked.connect(update_now)

    window.show()
    app.exec()

