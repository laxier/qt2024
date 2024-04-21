from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QDialog, QPushButton, QApplication, \
    QLabel
import pymysql.cursors


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ex 21: площадь трапеции")

        layout1 = QVBoxLayout()
        layout01 = QHBoxLayout()
        label1 = QLabel("первое основание")
        self.a_side = QLineEdit()
        layout01.addWidget(label1)
        layout01.addWidget(self.a_side)

        layout02 = QHBoxLayout()
        label2 = QLabel("второе основание")
        self.b_side = QLineEdit()
        layout02.addWidget(label2)
        layout02.addWidget(self.b_side)

        layout03 = QHBoxLayout()
        label3 = QLabel("высота")
        self.height = QLineEdit()
        layout03.addWidget(label3)
        layout03.addWidget(self.height)

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
        layout1.addLayout(layout03)
        layout1.addLayout(layout11)
        layout1.addLayout(layout12)
        layout1.addWidget(button_apply)
        self.setLayout(layout1)

    def reqdata(self):
        # """CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY,  FLOAT,  FLOAT,  FLOAT, Area FLOAT);""",
        a_side = float(self.a_side.text())
        b_side = float(self.b_side.text())
        height = float(self.height.text())

        surf = (a_side + b_side) * height / 2
        dbname_text = self.dbname.text()
        tablename_text = self.tname.text()
        sql = f"""INSERT INTO {tablename_text} (Base1, Base2, Height, Area) VALUES ('{a_side}', '{b_side}', '{height}', '{surf}');"""
        print(sql)
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
