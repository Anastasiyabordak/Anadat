import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QLineEdit, QMessageBox
import mysql.connector


class choseDatabase(QtWidgets.QMainWindow):

    def __init__(self, mainWindow, server):
        super().__init__()
        self.xData = []
        self.yData = []
        self.allTabsName = []
        self.alldatabases = []
        self.pages = []
        self.tabWidgets = []
        self.tableViews = []
        self.tabs = []
        self.mainWindow = mainWindow
        self.server = server
        self.initUI()

    def initUI(self):
        uic.loadUi("GUI/choseDatabase.ui", self)
        # get databases

        databases = "show databases"
        pass_databases = []
        cursor = self.server.cursor()
        cursor.execute(databases)
        for (databases) in cursor:
            pass_databases.append(databases[0])
        self.alldatabases = pass_databases
        font = QtGui.QFont()
        font.setFamily("Bitstream Charter")
        font.setPointSize(18)
        font.setItalic(True)
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setGeometry(QtCore.QRect(0, 0, 650, 640))
        self.toolBox.setObjectName("toolBox")
        self.toolBox.setFont(font)
        for i in range(0, len(pass_databases)):
            page = QtWidgets.QWidget()
            page.setGeometry(QtCore.QRect(0, 0, 650, 303))
            page.setObjectName(pass_databases[i])
            self.pages.append(page)
            self.toolBox.addItem(self.pages[i], "")
            self.toolBox.setItemText(i, pass_databases[i])
            tabWidget = QtWidgets.QTabWidget(self.pages[i])
            tabWidget.setGeometry(QtCore.QRect(0, 0, 650, 400))
            tabWidget.setObjectName("tabWidget")
            self.tabWidgets.append(tabWidget)
            cursor = self.server.cursor()  # get the cursor
            cursor.execute("USE "
                           + pass_databases[i])
            # select the database
            cursor.execute("SHOW TABLES")
            # execute 'SHOW TABLES' (but data is not returned)
            table_names = []
            for (table_name,) in cursor:
                table_names.append(table_name)
                self.allTabsName.append(table_name)
            for j in range(0, len(table_names)):
                tab = QtWidgets.QWidget(self.tabWidgets[i])
                tab.setObjectName("tab")
                self.tabs.append(tab)
                self.tabWidgets[i].addTab(tab, table_names[j])
                tableView = QtWidgets.QListWidget(tab)
                tableView.setGeometry(QtCore.QRect(0, 0, 650, 400))
                cursor.execute("SHOW columns FROM " + table_names[j])
                columns = []
                for column in cursor:
                    columns.append(column[0] + ' TYPE: ' + column[1])
                tableView.addItems(columns)
                tableView.itemClicked.connect(self.itemClickedList)
                self.tableViews.append(tableView)
        self.backButton.clicked.connect(self.showMainWindow)
        self.submitButton.clicked.connect(self.sendData)
        self.setFixedSize(1067, 654)
        self.show()

    def sendData(self):
        if len(self.xData) != len(self.yData):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Can't create plot, check len")
            msg.setWindowTitle("ERROR")
            msg.setStandardButtons(QMessageBox.Close)
            retval = msg.exec_()

    def itemClickedList(self, item):
        cwidget = self.sender().parent()
        listCTD = []

        listCTD.append(item.text().split(' ')[0])
        if 'decimal' in item.text().split(' ')[2] or 'int' in item.text().split(' ')[2]:
            for i in range(0, len(self.tabs)):
                if self.tabs[i] is cwidget:
                    listCTD.append(self.allTabsName[i])
            listCTD.append(self.alldatabases[self.toolBox.currentIndex()])
            msgBox = QMessageBox()
            msgBox.setText('What to do?')

            msgBox.addButton(QtWidgets.QPushButton('Abscissa'), QMessageBox.YesRole)  # 0
            msgBox.addButton(QtWidgets.QPushButton('Ordinate'), QMessageBox.NoRole)  # 1
            msgBox.addButton(QtWidgets.QPushButton('Cancel'), QMessageBox.RejectRole)  # 2
            ret = msgBox.exec_()
            if ret == 0:
                self.xData.append(listCTD)
                self.xEdit.insertPlainText(listCTD[2] + "." + listCTD[1] + "." + listCTD[0])
                self.xEdit.insertPlainText("\n")
            if ret == 1:
                self.yData.append(listCTD)
                self.yEdit.insertPlainText(listCTD[2] + "." + listCTD[1] + "." + listCTD[0])
                self.yEdit.insertPlainText("\n")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Can't create plot, check type")
            msg.setWindowTitle("ERROR")
            msg.setStandardButtons(QMessageBox.Close)
            retval = msg.exec_()

    # Back to main
    def showMainWindow(self):
        global main_ui
        self.mainWindow.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    global ex
    ex = MainWindow()
    a = app.exec_()
    sys.exit(a)
