import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QPushButton, QMessageBox
import pymysql.cursors

def find_even_indices(input_list):
    even_indices = [index for index, element in enumerate(input_list) if element % 2 == 0]
    return even_indices

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        layoutMAIN = QHBoxLayout()
        self.layout = QVBoxLayout()

        for i in range(20):
            line_edit = QLineEdit()
            line_edit.setMaxLength(3)  # Устанавливаем максимальную длину ввода в 3 символа
            line_edit.textChanged.connect(lambda text, le=line_edit: le.nextInFocusChain().setFocus() if len(text) > 2 else None)
            self.layout.addWidget(line_edit)
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

        layoutMAIN.addLayout(self.layout)
        layoutMAIN.addLayout(layout11)
        layoutMAIN.addLayout(layout12)
        layoutMAIN.addWidget(button_apply)
        self.setLayout(layoutMAIN)

    def reqdata(self):
        values = [int(self.layout.itemAt(i).widget().text()) for i in range(self.layout.count()) if self.layout.itemAt(i).widget()]
        result = find_even_indices(values)

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
                            List TEXT,
                            Even_indices TEXT
                        );"""
                cursor.execute(sql)
                sql = f"""INSERT INTO {tablename_text} (List, Even_indices) VALUES ('{str(values)}', '{str(result)}');"""
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
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())