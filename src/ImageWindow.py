from PyQt5 import QtWidgets
from PyQt5 import uic


class ImageWindow(QtWidgets.QMainWindow):

    def __init__(self, mainWindow):
        super().__init__()
        self.initUI()
        self.mainWindow = mainWindow

    def initUI(self):
        uic.loadUi("image.ui", self)
        operations = ['=', '<', '>']
        self.greenOperation.addItems(operations)
        self.blueOperation.addItems(operations)
        self.redOperation.addItems(operations)
        self.backButton.clicked.connect(self.showMainWindow)
        self.show()
        self.setFixedSize(882, 687)

    def showMainWindow(self):
        global main_ui
        # main_ui = MainWindow()
        self.mainWindow.show()
        self.close()
