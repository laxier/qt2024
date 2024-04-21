from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QDialog, QWidget, QComboBox, QPushButton, \
    QTableView, QApplication, QTabWidget, QTableWidget, QLabel
import numpy as np
import pymysql.cursors


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ex 19: matrix multiplier")
        layout1 = QVBoxLayout()
        layout01 = QHBoxLayout()
        self.label1 = QLabel("1 mat row cont")
        self.rowcount = QLineEdit()
        layout01.addWidget(self.label1)
        layout01.addWidget(self.rowcount)

        layout02 = QHBoxLayout()
        self.label2 = QLabel("1 mat col cont")
        self.colcount = QLineEdit()
        layout02.addWidget(self.label2)
        layout02.addWidget(self.colcount)

        layout03 = QHBoxLayout()
        self.label3 = QLabel("2 mat col cont")
        self.c2count = QLineEdit()
        layout03.addWidget(self.label3)
        layout03.addWidget(self.c2count)

        self.inputtable = QPushButton("adjust tables")
        self.inputtable.clicked.connect(self.updtable)
        self.printdata = QPushButton("multiply tables")
        self.printdata.clicked.connect(self.get_table_data)

        self.table1 = QTableWidget()
        self.table1.setColumnCount(2)
        self.table1.setRowCount(2)

        self.table2 = QTableWidget()
        self.table2.setColumnCount(2)
        self.table2.setRowCount(2)

        layout11 = QHBoxLayout()
        self.label4 = QLabel("DB name")
        self.dbname = QLineEdit()
        layout11.addWidget(self.label4)
        layout11.addWidget(self.dbname)

        layout12 = QHBoxLayout()
        self.label5 = QLabel("table name")
        self.tname = QLineEdit()
        layout12.addWidget(self.label5)
        layout12.addWidget(self.tname)

        layout1.addLayout(layout01)
        layout1.addLayout(layout02)
        layout1.addLayout(layout03)
        layout1.addWidget(self.inputtable)
        layout1.addWidget(self.table1)
        layout1.addWidget(self.table2)
        layout1.addLayout(layout11)
        layout1.addLayout(layout12)
        layout1.addWidget(self.printdata)
        self.setLayout(layout1)

    def updtable(self):
        try:
            r1count = int(self.rowcount.text())
            self.table1.setRowCount(r1count)
            c1count = int(self.colcount.text())
            self.table1.setColumnCount(c1count)
            r2count = int(self.colcount.text())
            self.table2.setRowCount(r2count)
            c2count = int(self.c2count.text())
            self.table2.setColumnCount(c2count)
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(None, "Error", error_message)

    def get_table_data(self):
        table1_data = []
        for row in range(self.table1.rowCount()):
            row_data = []
            for column in range(self.table1.columnCount()):
                item = self.table1.item(row, column)
                if item is not None:
                    row_data.append(int(item.text()))
                else:
                    row_data.append(0)
            table1_data.append(row_data)

        table2_data = []
        for row in range(self.table2.rowCount()):
            row_data = []
            for column in range(self.table2.columnCount()):
                item = self.table2.item(row, column)
                if item is not None:
                    row_data.append(int(item.text()))
                else:
                    row_data.append(0)
            table2_data.append(row_data)

        dbname_text = self.dbname.text()
        tablename_text = self.tname.text()

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='rootroot',
                                     charset='utf8mb4',
                                     database=dbname_text,
                                     cursorclass=pymysql.cursors.Cursor)
        try:
            result = np.dot(table1_data, table2_data).tolist()
            sql = f"""INSERT INTO {tablename_text} (Matrix1, Matrix2, Matrix3) VALUES ('{table1_data}', '{table2_data}', '{result}');"""
            print(sql)
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
            QMessageBox.information(None, "Success", "Entry was created!")
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(None, "Error", error_message)
        finally:
            connection.close()


if __name__ == '__main__':
    app = QApplication([])
    window = Main()
    window.show()
    app.exec()
