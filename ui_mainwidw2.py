import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import pymysql.cursors
import pandas as pd

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='rootroot',
                                     charset='utf8mb4',
                                     database="newnewnwenwe",
                                     cursorclass=pymysql.cursors.Cursor)

        print('Подключение к MySQL прошло успешно')
        with connection.cursor() as cursor:
            bdname = 'testtt'
            cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{bdname}'")
            header = [i[0] for i in cursor.fetchall()]
            cursor.execute(f"SELECT * FROM {bdname}")
            df = pd.DataFrame(cursor.fetchall(), columns=header)
        connection.close()

        self.model = TableModel(df)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec()
