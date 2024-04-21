from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QDialog, \
    QPushButton
from PyQt6.QtCore import pyqtSlot
import pymysql.cursors


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Degrees to Radians Converter')

        self.degrees_label = QLabel('Degrees:')
        self.degrees_input = QLineEdit()
        self.radians_label = QLabel('Radians:')
        self.radians_output = QLabel()

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
        layout.addWidget(self.degrees_label)
        layout.addWidget(self.degrees_input)
        layout.addWidget(self.radians_label)
        layout.addWidget(self.radians_output)
        layout.addLayout(layout11)
        layout.addLayout(layout12)
        layout.addWidget(button_apply)
        self.setLayout(layout)
        self.degrees_input.textChanged.connect(self.convert_degrees_to_radians)

    @pyqtSlot()
    def convert_degrees_to_radians(self):
        try:
            degrees = float(self.degrees_input.text())%360
            radians = degrees * (3.14159 / 180)  # конвертация градусов в радианы
            self.radians_output.setText(str(radians))
        except ValueError:
            self.radians_output.setText('Invalid input')

    def reqdata(self):
        degrees = float(self.degrees_input.text()) % 360
        radians = degrees * (3.14159 / 180)  # конвертация градусов в радианы
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
                            Degrees FLOAT,
                            Radians FLOAT
                        );"""
                print(sql)
                cursor.execute(sql)
                sql = f"""INSERT INTO {tablename_text} (Degrees, Radians) VALUES ('{degrees}', '{radians}');"""
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
