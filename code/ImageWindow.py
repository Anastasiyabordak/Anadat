from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
import imghdr


class ImageWindow(QtWidgets.QMainWindow):

    def __init__(self, mainWindow):
        super().__init__()
        self.initUI()
        self.mainWindow = mainWindow

    def initUI(self):
        uic.loadUi("GUI/image.ui", self)
        operations = ['=', '<', '>']
        self.greenOperation.addItems(operations)
        self.blueOperation.addItems(operations)
        self.redOperation.addItems(operations)
        self.backButton.clicked.connect(self.showMainWindow)
        self.openButton.clicked.connect(self.openImage)
        self.show()
        self.setFixedSize(882, 687)

    def showMainWindow(self):
        global main_ui
        # main_ui = MainWindow()
        self.mainWindow.show()
        self.close()

    def openImage(self):

# TODO
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName.lower().endswith(('.png', '.jpg', '.jpeg')) == True and len(fileName) != 0:
            pixmap = QPixmap(fileName)
            pixmap = pixmap.scaled(self.image.size(), QtCore.Qt.KeepAspectRatio)
            self.image.setPixmap(pixmap)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Can't open file")
            # msg.setInformativeText("T")
            msg.setWindowTitle("ERROR")
            msg.setDetailedText("File:" + fileName + " couldn't be opened. We support: *.png, *.jpg, *.jpeg")
            msg.setStandardButtons(QMessageBox.Close | QMessageBox.Ok)
            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                self.openImage()
            else:
                pass
