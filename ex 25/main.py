from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QDialog, \
    QPushButton
from PyQt6.QtCore import pyqtSlot
import pymysql.cursors


class Main(QDialog):
    def __init__(self):
        super().__init__()

        self.line_int = QLabel('line:')
        self.line = QLineEdit()
        self.line.setMaxLength(120)
        self.first20 = QLabel('first20:')
        self.first20_output = QLabel()

        self.last15 = QLabel('last 15:')
        self.last15_output = QLabel()

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

        button_apply = QPushButton("записать в таблицу")
        button_apply.clicked.connect(self.reqdata)

        layout = QVBoxLayout()
        layout.addWidget(self.line_int)
        layout.addWidget(self.line)
        layout.addWidget(self.first20)
        layout.addWidget(self.first20_output)
        layout.addWidget(self.last15)
        layout.addWidget(self.last15_output)
        layout.addLayout(layout11)
        layout.addLayout(layout12)
        layout.addWidget(button_apply)
        self.setLayout(layout)
        self.line.textChanged.connect(self.change_lines)

    @pyqtSlot()
    def change_lines(self):
        try:
            inputing = str(self.line.text())
            self.first20_output.setText(inputing[0:20])

        except ValueError:
            self.first20_output.setText('Invalid input')

        try:
            inputing = str(self.line.text())
            self.last15_output.setText(inputing[-15:])

        except ValueError:
            self.last15_output.setText('Invalid input')

    def reqdata(self):
        lister = self.line.text()
        listFirst =self.first20_output.text()
        listLast=self.last15_output.text()
        dbname_text = self.dbname.text()
        tablename_text = self.tname.text()

        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='rootroot',
                                         charset='utf8mb4',
                                         database=dbname_text,
                                         cursorclass=pymysql.cursors.Cursor)
            with connection.cursor() as cursor:
                sql = f"""CREATE TABLE IF NOT EXISTS {tablename_text} (
                            ID INT AUTO_INCREMENT PRIMARY KEY,
                            list TEXT,
                            listFirst TEXT,
                            listLast TEXT
                        );"""
                print(sql)
                cursor.execute(sql)
                sql = f"""INSERT INTO {tablename_text} (list, listFirst, listLast) VALUES ('{lister}', '{listFirst}', '{listLast}');"""
                print(sql)
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
