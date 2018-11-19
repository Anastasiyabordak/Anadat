from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from PyQt5 import QtGui
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt


class ImageWindow(QtWidgets.QMainWindow):

    def __init__(self, mainWindow):
        super().__init__()

        # image in RGB888
        self.imageValue = []
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

    # input_image = misc.imread('/home/anastasiya/Downloads/wifire/sd-3layers.jpg')

    # Method for changing image in GUI
    def setImage(self, input_image):
        height, width, channels = input_image.shape
        bytesPerLine = channels * width
        qImg = QtGui.QImage(input_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap = QPixmap(qImg)
        pixmap = pixmap.scaled(self.image.size(), QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(pixmap)

    # Back to main
    def showMainWindow(self):
        global main_ui
        # main_ui = MainWindow()

        self.mainWindow.show()
        self.close()

    def openImage(self):

        # TODO if image is already opened ask: continue or pass

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName.lower().endswith(('.png', '.jpg', '.jpeg')) == True and len(fileName) != 0:
            read_image = misc.imread(fileName)
            self.setImage(read_image)
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
