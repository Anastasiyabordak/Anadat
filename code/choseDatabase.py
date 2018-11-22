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
        try:
            server = mysql.connector.connect(user = self.loginEdit.toPlainText(),
                                        password = self.passwordEdit.text(),
                                        host = self.hostEdit.toPlainText())
            databases = ("show databases")
            pass_databases = []
            cursor = server.cursor()
            cursor.execute(databases)
            for (databases) in cursor:
                pass_databases.append(databases[0])
            print(pass_databases)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Unable to connect to MySQL server")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("SQL error")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    global ex
    ex = MainWindow()
    a = app.exec_()
    sys.exit(a)