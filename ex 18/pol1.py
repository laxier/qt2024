import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidget, QPushButton, QHBoxLayout

class TableInput(QWidget):
    def __init__(self):
        super().__init__()

        self.table1 = QTableWidget()
        self.table1.setRowCount(3)
        self.table1.setColumnCount(2)

        self.table2 = QTableWidget()
        self.table2.setRowCount(3)
        self.table2.setColumnCount(2)

        layout = QHBoxLayout()
        layout.addWidget(self.table1)
        layout.addWidget(self.table2)

        self.button = QPushButton('Get Table Data')
        self.button.clicked.connect(self.get_table_data)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.setWindowTitle('Table Input')
        self.show()

    def get_table_data(self):
        data1 = []
        data2 = []
        for row in range(self.table1.rowCount()):
            row_data = []
            for column in range(self.table1.columnCount()):
                item = self.table1.item(row, column)
                if item is not None:
                    row_data.append(float(item.text()))
                else:
                    row_data.append(0.0)
            data1.append(row_data)
        for row in range(self.table2.rowCount()):
            row_data = []
            for column in range(self.table2.columnCount()):
                item = self.table2.item(row, column)
                if item is not None:
                    row_data.append(float(item.text()))
                else:
                    row_data.append(0.0)
            data2.append(row_data)

        # result = [[data1[i][j] * data2[i][j] for j in range(len(data1[i]))] for i in range(len(data1))]
        sql = f"""-- INSERT INTO {tname} (Matrix1, Matrix2, Matrix3) VALUES ('{data1}', '{data2}', '{result}');"""
        # print(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableInput()
    sys.exit(app.exec())