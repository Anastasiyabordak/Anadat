from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QColorDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from PyQt5 import QtGui
import numpy as np
from scipy import misc
import operator
import matplotlib.pyplot as plt
from ImageStatus import ImageStatus

class ImageWindow(QtWidgets.QMainWindow):

    def __init__(self, mainWindow):
        super().__init__()

        # image in RGB888
        self.imageStatus = ImageStatus()
        self.imageValue = []
        self.initUI()
        self.mainWindow = mainWindow

    def initUI(self):
        # TODO add help button for RGB
        # TODO add help button for color

        uic.loadUi("GUI/image.ui", self)

        operations = ['>=', '<=', '=', '<', '>']
        self.greenOperation.addItems(operations)
        self.blueOperation.addItems(operations)
        self.redOperation.addItems(operations)
        self.colorButton.setStyleSheet("background-color: black");
        self.backButton.clicked.connect(self.showMainWindow)
        self.openButton.clicked.connect(self.openImage)
        self.setRGB.clicked.connect(self.RGBchange)
        self.colorButton.clicked.connect(self.changeColor)
        self.saveButton.clicked.connect(self.saveImage)
        self.show()
        self.setFixedSize(882, 687)

    # saving image
    def saveImage(self):
        if len(self.imageValue) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Image window is empty, open image first")
            msg.setWindowTitle("Saving error")
            msg.setStandardButtons(QMessageBox.Ok, QMessageBox.Cancel)
            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                self.openImageLoop()
            else:
                pass
        else:

            fileName, _ = QFileDialog.getSaveFileName()
            if len(fileName) != 0:
                misc.imsave(fileName, self.imageValue)

            pass

    # changing background Color
    def changeColor(self):
        color = QColorDialog.getColor()
        rgb = (color.red(), color.green(), color.blue())
        self.imageStatus.addSnapshotColor(rgb)
        self.colorButton.setStyleSheet("QWidget { background-color: rgb(%d,%d,%d) }" % rgb)
        self.setImage()

    # changing all RGB
    def RGBchange(self):
        # TODO change color
        if len(self.imageValue) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Image window is empty, open image first")
            msg.setWindowTitle("RGB error")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                self.openImageLoop()
            else:
                pass
            pass
        else:
            self.imageStatus.addSnapshotRGB([
                self.redEnter.value(),
                self.greenEnter.value(),
                self.blueEnter.value()
            ],
                [
                    self.redOperation.currentText(),
                    self.greenOperation.currentText(),
                    self.blueOperation.currentText()
                ])
            # process red
            if self.redOperation.currentText() == "<":
                self.imageValue[self.imageValue[:, :, 0] > self.redEnter.value()] = self.imageStatus.getColor()
            elif self.redOperation.currentText() == ">":
                self.imageValue[self.imageValue[:, :, 0] < self.redEnter.value()] = self.imageStatus.getColor()
            elif self.redOperation.currentText() == ">=":
                self.imageValue[self.imageValue[:, :, 0] <= self.redEnter.value()] = self.imageStatus.getColor()
            elif self.redOperation.currentText() == "<=":
                self.imageValue[self.imageValue[:, :, 0] >= self.redEnter.value()] = self.imageStatus.getColor()
            else:
                self.imageValue[self.imageValue[:, :, 0] != self.redEnter.value()] = self.imageStatus.getColor()
            # process green
            if self.greenOperation.currentText() == "<":
                self.imageValue[self.imageValue[:, :, 1] > self.greenEnter.value()] = self.imageStatus.getColor()
            elif self.greenOperation.currentText() == ">":
                self.imageValue[self.imageValue[:, :, 1] < self.greenEnter.value()] = self.imageStatus.getColor()
            elif self.greenOperation.currentText() == ">=":
                self.imageValue[self.imageValue[:, :, 1] <= self.greenEnter.value()] = self.imageStatus.getColor()
            elif self.greenOperation.currentText() == "<=":
                self.imageValue[self.imageValue[:, :, 1] >= self.greenEnter.value()] = self.imageStatus.getColor()
            else:
                self.imageValue[self.imageValue[:, :, 1] != self.greenEnter.value()] = self.imageStatus.getColor()
            # process blue
            if self.blueOperation.currentText() == "<":
                self.imageValue[self.imageValue[:, :, 2] > self.blueEnter.value()] = self.imageStatus.getColor()
            elif self.blueOperation.currentText() == ">":
                self.imageValue[self.imageValue[:, :, 2] < self.blueEnter.value()] = self.imageStatus.getColor()
            elif self.blueOperation.currentText() == ">=":
                self.imageValue[self.imageValue[:, :, 2] <= self.blueEnter.value()] = self.imageStatus.getColor()
            elif self.blueOperation.currentText() == "<=":
                self.imageValue[self.imageValue[:, :, 2] >= self.blueEnter.value()] = self.imageStatus.getColor()
            else:
                self.imageValue[self.imageValue[:, :, 2] != self.blueEnter.value()] = self.imageStatus.getColor()
            self.setImage()

    # Method for changing image in GUI
    def setImage(self):
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
        if len(self.imageValue) == 0:  # if image is not open, enter loop
            self.openImageLoop()
        else:  # if image was opened - ask: continue or open another image
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("You process image right now. Do you want to open another image?")
            msg.setWindowTitle("Are you sure?")
            msg.setStandardButtons(QMessageBox.Close | QMessageBox.Ok)
            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                # TODO new image - clean rgb
                # TODO add to snapshot
                self.openImageLoop()
            else:
                pass

    # loop openImage, fail - another iteration
    def openImageLoop(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select dir", "",
                                                  "All Files (*)", options=options)
        # checking is file an image
        if fileName.lower().endswith(('.png', '.jpg', '.jpeg')) == True and len(fileName) != 0:
            if len(self.imageValue) != 0:
                self.imageValue = misc.imread(fileName)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Reset prev RGB value and Operations?")
                msg.setWindowTitle("RGB")
                msg.setStandardButtons(QMessageBox.No | QMessageBox.Ok)
                retval = msg.exec_()
                if retval == QMessageBox.Ok:
                    #self.changeColor()
                    print("reset RGB")
                    # TODO add reset RGB
            else:
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
                self.openImageLoop()
            else:
                pass
