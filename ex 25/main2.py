from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QDialog, QWidget, QComboBox, QPushButton, \
    QTableView, QApplication, QTabWidget
from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, pyqtSignal
import pymysql.cursors
import pandas as pd
import datetime


# для отображения таблицы из пандас
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        # Retrieve the data to be displayed at the specified index and role
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        # Return the number of rows in the model
        return self._data.shape[0]

    def columnCount(self, index):
        # Return the number of columns in the model
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # Retrieve the header data for the specified section, orientation, and role
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])


def get_dbases():
    # Establish connection to MySQL server
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='rootroot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.Cursor)

    # Retrieve list of databases
    with connection.cursor() as cursor:
        cursor.execute("show databases")
        dbases = [i[0] for i in cursor.fetchall()]
    connection.close()
    return dbases


def get_tables(dbname):
    # Establish connection to specific database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='rootroot',
                                 charset='utf8mb4',
                                 database=dbname,
                                 cursorclass=pymysql.cursors.Cursor)

    # Retrieve list of tables in the database
    with connection.cursor() as cursor:
        cursor.execute("show tables")
        tables = [i[0] for i in cursor.fetchall()]
    connection.close()
    return tables


def heads(dbname, tbname):
    # Establish connection to specific database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='rootroot',
                                 charset='utf8mb4',
                                 database=dbname,
                                 cursorclass=pymysql.cursors.Cursor)
    with connection.cursor() as cursor:
        # Retrieve list table fields name
        cursor.execute(
            f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tbname}' ORDER BY ORDINAL_POSITION")
        header = [i[0] + " " + i[1] for i in cursor.fetchall()]
    connection.close()
    return header


def get_table(bdname, tname):
    # Establish connection to specific database and table
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='rootroot',
                                 charset='utf8mb4',
                                 database=bdname,
                                 cursorclass=pymysql.cursors.Cursor)

    with connection.cursor() as cursor:
        # Retrieve column names of the table
        cursor.execute(
            f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tname}' ORDER BY ORDINAL_POSITION")
        header = [i[0] for i in cursor.fetchall()]

        # Retrieve data from the table and create a pandas dataframe
        cursor.execute(f"SELECT * FROM {tname}")
        df = pd.DataFrame(cursor.fetchall(), columns=header)
    connection.close()
    return df


def get_table_excel(bdname, tname):
    # Establish connection to specific database and table
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='rootroot',
                                 charset='utf8mb4',
                                 database=bdname,
                                 cursorclass=pymysql.cursors.Cursor)

    with connection.cursor() as cursor:
        # Retrieve column names of the table
        cursor.execute(
            f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tname}' ORDER BY ORDINAL_POSITION")
        header = [i[0] for i in cursor.fetchall()]

        # Retrieve data from the table and create a pandas dataframe
        cursor.execute(f"SELECT * FROM {tname}")
        df = pd.DataFrame(cursor.fetchall(), columns=header)

    connection.close()

    # Generate a unique filename based on database name, table name, and current datetime
    current_datetime = datetime.datetime.now()
    current_datetime_string = current_datetime.strftime("%Y-%m-%d %H-%M-%S")
    name = bdname + " " + tname + " " + current_datetime_string + ".xlsx"

    # Save the dataframe as an Excel file
    df.to_excel(name, index=False)
    return


class Main(QDialog):
    tableUpdating = pyqtSignal()  # Signal for updating the table
    DBUpdating = pyqtSignal()  # Signal for updating the database
    TableUPD = pyqtSignal()  # Signal for updating the table

    def __init__(self):
        super().__init__()

        uic.loadUi("untitled.ui", self)

        # using the self.findChild() method to search for specific UI elements within the current object
        self.selectDB = self.findChild(QComboBox, "selectDB")
        self.selectTable = self.findChild(QComboBox, "selectTable")
        updater = self.findChild(QPushButton, "updater")
        self.table = self.findChild(QTableView, "table")
        newent = self.findChild(QPushButton, "newent")
        exporter = self.findChild(QPushButton, "exporter")
        newbd = self.findChild(QPushButton, "newbd")
        newtable = self.findChild(QPushButton, "newtable")

        self.upd_db()  # Call the method to update the database
        self.upd_tb()  # Call the method to update the table
        # Connect signals to slots
        self.selectDB.currentTextChanged.connect(self.on_combobox_changed)
        updater.clicked.connect(self.update_now)
        newent.clicked.connect(self.on_pushButton_clicked)
        exporter.clicked.connect(self.import_xlsx)
        newbd.clicked.connect(self.newbd_function)
        newtable.clicked.connect(self.newtable_function)

    def upd_db(self):
        """
        Update the table dropdown menu with the databases.
        """
        self.db = get_dbases()  # Getting the updated list of databases

        # Getting a list of all items currently in selectDB ComboBox
        all_items = [self.selectDB.itemText(i) for i in range(self.selectDB.count())]

        for item in self.db:
            # Checking if the item already exists in the ComboBox, add if doesn't
            if item not in all_items:
                self.selectDB.addItem(item)
        return

    def upd_tb(self):
        """
        Update the table dropdown menu with the tables in the selected database.
        """
        self.selectTable.clear()  # Clear the dropdown menu
        dbname = self.selectDB.currentText()  # Get the selected database name from the dropdown menu
        self.selectTable.addItems(get_tables(dbname))  # Add the tables from the selected database to the dropdown menu
        return

    def on_combobox_changed(self):
        """
        This function is called when the selected database is changed
        """
        # Update the table dropdown menu with the tables in the selected database
        dbname = self.selectDB.currentText()
        self.selectTable.clear()
        self.selectTable.addItems(get_tables(dbname))
        return

    def update_now(self):
        """
        responsible for updating the table view with the data from the selected database and table
        """
        dbname = self.selectDB.currentText()
        tname = self.selectTable.currentText()
        try:
            model = TableModel(get_table(dbname, tname))
            self.table.setModel(model)
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(None, "Error", error_message)
        return

    def on_pushButton_clicked(self):
        # Open a new window for adding a new entry to the selected table
        self.sec = Second(self.selectDB, self.selectTable)
        self.sec.tableUpdating.connect(self.update_now)
        self.sec.show()

    def import_xlsx(self):
        # Get the selected database and table names
        dbname = self.selectDB.currentText()
        tname = self.selectTable.currentText()
        try:
            # Call the "get_table_excel" function with "dbname" and "tname" arguments
            get_table_excel(dbname, tname)
            QMessageBox.information(None, "Success", "File was created!")
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(None, "Error", error_message)

    def newbd_function(self):
        # Open a new window for creating a new database
        self.BD = CreateBD()
        self.BD.DBUpdating.connect(self.upd_db)
        self.BD.show()

    def newtable_function(self):
        # Open a new window for creating a new table in the selected database
        self.tablewindow = CreateTable(self.selectDB)
        self.tablewindow.TableUPD.connect(self.upd_tb)
        self.tablewindow.show()


class CreateBD(QWidget):
    # Define a custom signal to indicate that the databases list has been updated
    DBUpdating = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("DB name")
        button_send = QPushButton("Create")

        layout = QVBoxLayout(self)
        layout.addWidget(self.lineEdit)
        layout.addWidget(button_send)

        button_send.clicked.connect(self.create_bd)

    def create_bd(self):
        # Get database name from lineEdit input
        dbname = self.lineEdit.text()

        # Establish a connection to the MySQL server
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='rootroot',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.Cursor)

        try:
            with connection.cursor() as cursor:
                sql = f"CREATE DATABASE {dbname}"
                cursor.execute(sql)
                connection.commit()
            QMessageBox.information(None, "Success", "DataBase created")
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(None, "Error", error_message)
        finally:
            connection.close()
        self.DBUpdating.emit()  # Emit the custom signal to indicate that the database has been updated
        self.close()


class CreateTable(QWidget):
    # Define a custom signal to indicate that the table list has been updated
    TableUPD = pyqtSignal()

    # Define global variable for MySQL data types
    global mysql_data_types
    mysql_data_types = [
        'INT',
        'VARCHAR(255)',
        'FLOAT'
        'DOUBLE',
        'DATE',
        'DATETIME',
        'TIMESTAMP',
        'BOOLEAN'
    ]

    def __init__(self, selectDB):
        super().__init__()
        self.layout0 = QVBoxLayout()
        self.dbname = selectDB.currentText()  # Set the value of self.dbname to selectDB from mainwindow

        button1 = QPushButton('Add New Field')
        button1.clicked.connect(self.add_new_line)

        self.tablename = QLineEdit()
        self.tablename.setPlaceholderText("Enter the table name")

        button2 = QPushButton('Create table')
        button2.clicked.connect(self.createTBLE)

        # Create a QWidget for the first tab
        tab1widget = QWidget()
        self.tab1layout = QVBoxLayout()
        self.tab1layout.addWidget(self.tablename)
        self.tab1layout.addWidget(button1)
        self.tab1layout.addWidget(button2)
        tab1widget.setLayout(self.tab1layout)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(tab1widget, "table")  # Add tab1widget to the QTabWidget with the label "table"

        # Create the second tab, for the templated table
        tab2 = QWidget()
        layout2 = QVBoxLayout(tab2)
        self.tablename2 = QLineEdit()
        self.tablename2.setPlaceholderText("Enter the table name")

        # Define the templates for table creation
        self.templates = {
            "furniture": """CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY, Date_of_delivery DATE, Department VARCHAR(255), Furniture_type VARCHAR(255), Furniture_price VARCHAR(255));""",
            "matrices": """CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY, Matrix1 VARCHAR(255), Matrix2 VARCHAR(255), Matrix3 VARCHAR(255));""",
            "person": """CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY, Full_Name VARCHAR(255), Date_of_Birth DATE, Days_Lived INT);""",
            "trapezoid": """CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY, Base1 FLOAT, Base2 FLOAT, Height FLOAT, Area FLOAT);""",
            "angles": """CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY, Degrees FLOAT, Radians FLOAT);"""
        }

        self.templates_box = QComboBox()
        self.templates_box.addItems(self.templates.keys())

        # Create a QPushButton to trigger the table creation
        button3 = QPushButton('Create table')
        button3.clicked.connect(self.createTBLE2)

        # Add the widgets to the layout
        layout2.addWidget(self.tablename2)
        layout2.addWidget(self.templates_box)
        layout2.addWidget(button3)

        # Add the second tab to the QTabWidget
        self.tab_widget.addTab(tab2, "create by the Template")

        # Add the QTabWidget to the main layout
        self.layout0.addWidget(self.tab_widget)
        self.setLayout(self.layout0)

    def add_new_line(self):
        self.line_edit = QLineEdit()

        self.combobox = QComboBox()
        self.combobox.addItems(mysql_data_types)

        # Create a horizontal layout to organize the line edit and combo box side by side
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.line_edit)
        self.horizontal_layout.addWidget(self.combobox)

        # Add the horizontal layout to the main layout
        self.tab1layout.addLayout(self.horizontal_layout)

    def createTBLE(self):
        try:
            element_list = []
            # Iterate over the layouts starting from index 3
            for i in range(len(self.tab1layout))[3::]:
                horizontal_layout = self.tab1layout.itemAt(i).layout()

                # Get the left element (field name) and right element (field type) from the horizontal layout
                field_name = horizontal_layout.itemAt(0).widget()
                field_type = horizontal_layout.itemAt(1).widget()
                element_list.append([field_name.text(), field_type.currentText()])

            # Create the SQL query to create the table
            sql = f"CREATE TABLE {self.tablename.text()} ("
            for field in element_list:
                field_name = field[0]
                field_type = field[1]
                sql += f"{field_name} {field_type}, "
            sql = sql.rstrip(", ") + ")"

            print(sql)
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(None, "Error", error_message)


        # Create a connection to the database server
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='rootroot',
                                     charset='utf8mb4',
                                     database=self.dbname,
                                     cursorclass=pymysql.cursors.Cursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(None, "Error", error_message)
        finally:
            connection.close()
        self.TableUPD.emit()  # Emit the custom signal to indicate that the tables list has been updated
        self.close()

    def createTBLE2(self):
        curr_template = self.templates_box.currentText()
        table_name = self.tablename2.text()

        sql = self.templates[curr_template].format(table_name)
        print(sql)
        # Create a connection to the database server
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='rootroot',
                                     charset='utf8mb4',
                                     database=self.dbname,
                                     cursorclass=pymysql.cursors.Cursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(None, "Error", error_message)
        finally:
            connection.close()
        self.TableUPD.emit()  # Emit the custom signal to indicate that the tables list has been updated
        self.close()


class Second(QWidget):
    # Define a custom signal to indicate that the table list has been updated
    tableUpdating = pyqtSignal()

    def __init__(self, selectDB, selectTable):
        super().__init__()

        # Get the selected database and table names from the combo boxes
        self.dbname = selectDB.currentText()
        self.tbname = selectTable.currentText()

        # Get the header (column names and data types) of the table
        self.header = heads(self.dbname, self.tbname)
        self.layout = QVBoxLayout(self)

        # Create line edit widgets for each column in the table
        for element in self.header:
            self.lineEdit = QLineEdit()
            self.lineEdit.setPlaceholderText(element)
            self.layout.addWidget(self.lineEdit)

        self.button_send = QPushButton("Create")
        self.layout.addWidget(self.button_send)
        self.button_send.clicked.connect(self.access_widget)

    def access_widget(self):
        inp_data = []
        for i in range(len(self.header)):
            inp_data.append(self.layout.itemAt(i).widget().text())

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='rootroot',
                                     charset='utf8mb4',
                                     database=self.dbname,
                                     cursorclass=pymysql.cursors.Cursor)

        try:
            with connection.cursor() as cursor:
                placeholders = ', '.join(['%s'] * len(inp_data))
                # Execute the SQL query to insert a new entry into the table
                sql = f"INSERT INTO {self.tbname} VALUES ({placeholders})"
                cursor.execute(sql, tuple(inp_data))
                connection.commit()
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(None, "Error", error_message)
        finally:
            connection.close()
        self.tableUpdating.emit()  # Emit the custom signal to indicate that the tables have been updated
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = Main()
    window.show()
    app.exec()
