import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QLineEdit,QMessageBox
import mysql.connector

class choseDatabase(QtWidgets.QMainWindow):

    def __init__(self, mainWindow,server):
        super().__init__()
        self.mainWindow = mainWindow
        self.server= server
        self.initUI()

    def initUI(self):
        uic.loadUi("GUI/choseDatabase.ui", self)
        databases = ("show databases")
        pass_databases = []
        cursor = self.server.cursor()
        cursor.execute(databases)
        for (databases) in cursor:
            pass_databases.append(databases[0])
        self.comboBox.addItems(pass_databases)
        self.backButton.clicked.connect(self.showMainWindow)
        self.submitButton.clicked.connect(self.choseData)
        self.show()
        self.setFixedSize(542, 277)

    # Back to main
    def showMainWindow(self):
        global main_ui
        self.mainWindow.show()
        self.close()
    def choseData(self):
        
        cursor = self.server.cursor()     # get the cursor
        print("USE " + self.comboBox.currentText())
        cursor.execute("USE " + self.comboBox.currentText()) # select the database
        cursor.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)
        #tables = cursor.fetchall() # get last query
        table_names = []
        for (table_name,) in cursor:
            print("TABLE NAME",table_name)
            table_names.append(table_name)
        for table_name in table_names:
            print("TABLE NAME",table_name)
            cursor.execute("SHOW columns FROM " + table_name)
            print("Column names:")
            for column in cursor:
                print(column)     
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    global ex
    ex = MainWindow()
    a = app.exec_()
    sys.exit(a)