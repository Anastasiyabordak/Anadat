import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
from ImageWindow import ImageWindow
from LoginWindow import LoginWindow

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("GUI/startPage.ui", self)
        self.imageButton.clicked.connect(self.showImageWindow)
        self.sqlButton.clicked.connect(self.showLoginWindow)
        self.show()
        self.setFixedSize(210, 210)

    def showImageWindow(self):
        global image_ui
        image_ui = ImageWindow(ex)
        image_ui.show()
        self.close()

    def showLoginWindow(self):
        global login_ui
        login_ui = LoginWindow(ex)
        login_ui.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    global ex
    ex = MainWindow()
    a = app.exec_()
    sys.exit(a)
