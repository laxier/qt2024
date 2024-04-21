import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tab Widget Example")

        self.tab_widget = QTabWidget()

        tab1 = QWidget()

        self.layout = QVBoxLayout(tab1)
        self.dbname = "polina"

        self.button1 = QPushButton('Add New Field')
        self.button1.clicked.connect(self.add_new_line)

        self.tablename = QLineEdit()
        self.tablename.setPlaceholderText("Enter the table name")

        self.button2 = QPushButton('Create table')
        self.button2.clicked.connect(self.createTBLE)

        # Add the widgets to the layout
        self.layout.addWidget(self.tablename)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)

        tab2 = QWidget()
        layout2 = QVBoxLayout(tab2)
        label2 = QLabel("Hello from Tab 2")
        layout2.addWidget(label2)

        self.tab_widget.addTab(tab1, "Tab 1")
        self.tab_widget.addTab(tab2, "Tab 2")

        self.setCentralWidget(self.tab_widget)

    def add_new_line(self):
        # Add functionality for the "Add New Field" button here
        pass

    def createTBLE(self):
        # Add functionality for the "Create table" button here
        pass


# Create an instance of the MyWindow class
app = QApplication(sys.argv)
window = MyWindow()
window.show()

# Run the application's event loop
sys.exit(app.exec())