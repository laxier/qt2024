import sys
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QDialog, QWidget, QComboBox, QPushButton, \
    QTableView, QApplication, QMainWindow, QTabWidget, QLabel
from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, pyqtSignal
import pymysql.cursors
import pandas as pd

class Main(QDialog):
    tableUpdating = pyqtSignal()  # Signal for updating the table
    DBUpdating = pyqtSignal()  # Signal for updating the database
    TableUPD = pyqtSignal()  # Signal for updating the table

    def __init__(self):
        super().__init__()

        uic.loadUi("untitled.ui", self)

        _updater = self.findChild(QPushButton, "updater")
        _updater.setText("Hello")


app = QApplication(sys.argv)
window = Main()
window.show()
sys.exit(app.exec())
