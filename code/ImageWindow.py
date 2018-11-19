from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from PyQt5 import QtGui
import numpy as np
from scipy import misc
import  operator
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
        operations = ['>=', '<=','=', '<', '>']
        self.greenOperation.addItems(operations)
        self.blueOperation.addItems(operations)
        self.redOperation.addItems(operations)
        self.backButton.clicked.connect(self.showMainWindow)
        self.openButton.clicked.connect(self.openImage)
        self.show()
        self.redEnter.valueChanged.connect(self.RGBchange)
        self.blueEnter.valueChanged.connect(self.RGBchange)
        self.greenEnter.valueChanged.connect(self.RGBchange)
        self.redOperation.currentIndexChanged.connect(self.RGBchange)
        self.blueOperation.currentIndexChanged.connect(self.RGBchange)
        self.greenOperation.currentIndexChanged.connect(self.RGBchange)
        self.setFixedSize(882, 687)

# changing all RGB
    def RGBchange(self):
        # TODO check image is open
        # process red
        if self.redOperation.currentText() == "<":
            self.imageValue[self.imageValue[:, :, 0] < self.redEnter.value()] = 0
        elif self.redOperation.currentText() == ">":
            self.imageValue[self.imageValue[:, :, 0] > self.redEnter.value()] = 0
        elif self.redOperation.currentText() == ">=":
            self.imageValue[self.imageValue[:, :, 0] >= self.redEnter.value()] = 0
        elif self.redOperation.currentText() == "<=":
            self.imageValue[self.imageValue[:, :, 0] <= self.redEnter.value()] = 0
        else:
            self.imageValue[self.imageValue[:, :, 0] == self.redEnter.value()] = 0
        # process green
        if self.greenOperation.currentText() == "<":
            self.imageValue[self.imageValue[:, :, 1] < self.greenEnter.value()] = 0
        elif self.greenOperation.currentText() == ">":
            self.imageValue[self.imageValue[:, :, 1] > self.greenEnter.value()] = 0
        elif self.greenOperation.currentText() == ">=":
            self.imageValue[self.imageValue[:, :, 1] >= self.greenEnter.value()] = 0
        elif self.greenOperation.currentText() == "<=":
            self.imageValue[self.imageValue[:, :, 1] <= self.greenEnter.value()] = 0
        else:
            self.imageValue[self.imageValue[:, :, 1] == self.greenEnter.value()] = 0
        # process blue
        if self.blueOperation.currentText() == "<":
            self.imageValue[self.imageValue[:, :, 2] < self.blueEnter.value()] = 0
        elif self.blueOperation.currentText() == ">":
            self.imageValue[self.imageValue[:, :, 2] > self.blueEnter.value()] = 0
        elif self.blueOperation.currentText() == ">=":
            self.imageValue[self.imageValue[:, :, 2] >= self.blueEnter.value()] = 0
        elif self.blueOperation.currentText() == "<=":
            self.imageValue[self.imageValue[:, :, 2] <= self.blueEnter.value()] = 0
        else:
            self.imageValue[self.imageValue[:, :, 2] == self.blueEnter.value()] = 0
        self.setImage()
    # Method for changing image in GUI
    def setImage(self):
        print(self.imageValue.shape)
        height, width, channels = self.imageValue.shape
        bytesPerLine = channels * width
        qImg = QtGui.QImage(self.imageValue.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap = QPixmap(qImg)
        pixmap = pixmap.scaled(self.image.size(), QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(pixmap)

    # Back to main
    def showMainWindow(self):
        global main_ui
        self.mainWindow.show()
        self.close()

    #  opening image handling
    def openImage(self):

        # TODO if image is already opened ask: continue or pass

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        # checking is file an image
        if fileName.lower().endswith(('.png', '.jpg', '.jpeg')) == True and len(fileName) != 0:
            self.imageValue = misc.imread(fileName)
            self.setImage()
        # if file is not an image - show message box. Ok - continue opening, Close - abort
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
