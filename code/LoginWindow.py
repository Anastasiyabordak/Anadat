import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QLineEdit, QMessageBox
import mysql.connector
from choseDatabase import choseDatabase


class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.initUI()

    def initUI(self):
        uic.loadUi("GUI/login.ui", self)
        self.backButton.clicked.connect(self.showMainWindow)
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.submitButton.clicked.connect(self.connectDatabase)
        self.show()
        self.setFixedSize(542, 277)

    # Back to main
    def showMainWindow(self):
        global main_ui
        self.mainWindow.show()
        self.close()

    def connectDatabase(self):
        try:
            server = mysql.connector.connect(user=self.loginEdit.toPlainText(),
                                             password=self.passwordEdit.text(),
                                             host=self.hostEdit.toPlainText())
            global choseDatabase_ui
            choseDatabase_ui = choseDatabase(self.mainWindow, server)
            choseDatabase_ui.show()
            self.close()
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
