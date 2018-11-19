import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from ImageWindow import ImageWindow

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("startPage.ui", self)
        self.imageButton.clicked.connect(self.showImageWindow)
        self.show()
        self.setFixedSize(210,210)


    def showImageWindow(self):
        global  image_ui
        image_ui = ImageWindow(ex)
        image_ui.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    global ex
    ex = MainWindow()
    a = app.exec_()
    sys.exit(a)
