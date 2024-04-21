from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QDialog, QPushButton, QApplication, \
    QLabel, QCalendarWidget
from datetime import date
import pymysql.cursors


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ex 21: Радианы и градусы")
        layout1 = QVBoxLayout()
        layout01 = QHBoxLayout()
        label1 = QLabel("угол в градусах")
        self.fio = QLineEdit()
        layout01.addWidget(label1)
        layout01.addWidget(self.fio)

        layout02 = QVBoxLayout()
        label2 = QLabel("Дата рождения")
        self.calend = QCalendarWidget()
        self.calend.setGridVisible(True)
        layout02.addWidget(label2)
        layout02.addWidget(self.calend)

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

        layout1.addLayout(layout01)
        layout1.addLayout(layout02)
        layout1.addLayout(layout11)
        layout1.addLayout(layout12)
        layout1.addWidget(button_apply)
        self.setLayout(layout1)

    def reqdata(self):
        name = self.fio.text()
        birth = self.calend.selectedDate().toPyDate()
        curr_days = (date.today() - birth).days

        dbname_text = self.dbname.text()
        tablename_text = self.tname.text()
        sql = f"""INSERT INTO {tablename_text} (Full_Name, Date_of_Birth, Days_Lived) VALUES ('{name}', '{birth}', '{curr_days}');"""

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='rootroot',
                                     charset='utf8mb4',
                                     database=dbname_text,
                                     cursorclass=pymysql.cursors.Cursor)
        try:
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
