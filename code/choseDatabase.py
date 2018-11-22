import sys
from PyQt5 import QtWidgets, QtGui,QtCore
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
#get databases

        databases = ("show databases")
        pass_databases = []
        cursor = self.server.cursor()
        cursor.execute(databases)
        for (databases) in cursor:
            pass_databases.append(databases[0])
        font = QtGui.QFont()
        font.setFamily("Bitstream Charter")
        font.setPointSize(18)
        font.setItalic(True)

        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setGeometry(QtCore.QRect(0, 0, 650, 640))
        self.toolBox.setObjectName("toolBox")
        self.toolBox.setFont(font)
        self.pages = []
        self.tabWidgets = []
        self.tabs = []
        self.tableViews = []
        for i in range(0,len(pass_databases)):
            page = QtWidgets.QWidget()
            page.setGeometry(QtCore.QRect(0, 0, 650, 303))
            page.setObjectName(pass_databases[i])
            self.pages.append(page)
            self.toolBox.addItem(self.pages[i], "")
            self.toolBox.setItemText(i,pass_databases[i])
            tabWidget = QtWidgets.QTabWidget(self.pages[i])
            tabWidget.setGeometry(QtCore.QRect(0, 0, 650, 400))
            tabWidget.setObjectName("tabWidget")
            self.tabWidgets.append(tabWidget)
            cursor = self.server.cursor()     # get the cursor
            cursor.execute("USE " + pass_databases[i]) # select the database
            cursor.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)
            table_names = []
            for (table_name,) in cursor:
                table_names.append(table_name)
            for j in range(0, len(table_names)):
                tab = QtWidgets.QWidget(self.tabWidgets[i])
                tab.setObjectName("tab")
                self.tabs.append(tab)
                print(table_names[j])
                print(len(self.tabs))
                self.tabWidgets[i].addTab(tab, table_names[j])
                #tableView = QtWidgets.QTableView(self.tabs[i])
                #tableView.setGeometry(QtCore.QRect(20, 20, 391, 160))
                #self.tableViews.append(tableView)
            print(self.tabWidgets[i].count())
        self.comboBox.addItems(pass_databases)
        self.backButton.clicked.connect(self.showMainWindow)
        self.submitButton.clicked.connect(self.choseData)
        self.setFixedSize(953, 674)
        self.show()


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