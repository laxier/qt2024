import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("template.ui",self)

        # people = [{"name": "John", "age": 45, "address": "New York"}, {"name": "Mark", "age": 40, "address": "LA"},
        #           {"name": "George", "age": 30, "address": "London"}]
        # row = 0
        # self.tableWidget.setRowCount(len(people))
        # for person in people:
        #     self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(person["name"]))
        #     self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(person["age"])))
        #     self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(person["address"]))
        #     row = row + 1



# main
app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(850)
widget.setFixedWidth(1120)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")