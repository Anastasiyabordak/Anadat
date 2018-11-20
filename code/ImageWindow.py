from PyQt5 import QtWidgets
from PyQt5.Qt import QApplication
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
        self.flag = False
        #image that displayed for user
        self.imageValue = []
        self.initUI()
        self.mainWindow = mainWindow


    def initUI(self):
        uic.loadUi("GUI/image.ui", self)

        self.operations = ['>=', '<=', '=', '<', '>']
        self.greenOperation.addItems(self.operations)
        self.blueOperation.addItems(self.operations)
        self.redOperation.addItems(self.operations)
        self.colorButton.setStyleSheet("background-color: black");
        self.backButton.clicked.connect(self.showMainWindow)
        self.openButton.clicked.connect(self.openImage)
        self.redEnter.valueChanged.connect(self.RGBchange)
        self.blueEnter.valueChanged.connect(self.RGBchange)
        self.greenEnter.valueChanged.connect(self.RGBchange)
        self.redOperation.currentIndexChanged.connect(self.RGBchange)
        self.blueOperation.currentIndexChanged.connect(self.RGBchange)
        self.greenOperation.currentIndexChanged.connect(self.RGBchange)
        self.colorButton.clicked.connect(self.changeColor)
        self.saveButton.clicked.connect(self.saveImage)
        self.undoButton.clicked.connect(self.undo)
        self.copyButton.clicked.connect(self.copyClipboard)
        self.show()
        self.setFixedSize(882, 687)
    def copyClipboard(self):
        height, width, channels = self.imageValue.shape
        bytesPerLine = channels * width
        qImg = QtGui.QImage(self.imageValue.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        QApplication.clipboard().setImage(qImg)
        pass
    def undo(self):
        print(self.imageStatus.currentIndex)
        if self.imageStatus.setUndo() == True:
            if self.imageStatus.currentIndex == 0:
                self.imageValue = []
                self.image.clear()
                self.redEnter.setValue(0)
                self.blueEnter.setValue(0)
                self.greenEnter.setValue(0)
                self.blueOperation.setCurrentIndex(0)
                self.greenOperation.setCurrentIndex(0)
                self.redOperation.setCurrentIndex(0)
                self.colorButton.setStyleSheet("background-color: black")
            else:
                print("After0", self.imageStatus.currentIndex)
                temp = self.imageStatus.getRGB()
                self.flag = True
                self.redEnter.setValue(temp[0])
                self.blueEnter.setValue(temp[1])
                self.greenEnter.setValue(temp[2])
                self.blueOperation.setCurrentIndex(self.operations.index(temp[3]))
                self.greenOperation.setCurrentIndex(self.operations.index(temp[4]))
                self.redOperation.setCurrentIndex(self.operations.index(temp[5]))
                self.flag = False
                self.RGBchange()
                self.setImage()
                self.imageStatus.removeDub()
                rgb = self.imageStatus.getColor()
                self.colorButton.setStyleSheet("QWidget { background-color: rgb(%d,%d,%d) }" % rgb)
                print("After", self.imageStatus.currentIndex)

        else:
            # TODO add message Box
            print("Unable")

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
                try:
                    misc.imsave(fileName, self.imageValue)
                except Exception as e:
                    print(e)

            pass

    # changing background Color
    def changeColor(self):
        color = QColorDialog.getColor()
        rgb = (color.red(), color.green(), color.blue())
        self.imageStatus.addSnapshotColor(rgb)
        self.colorButton.setStyleSheet("QWidget { background-color: rgb(%d,%d,%d) }" % rgb)

    # changing all RGB
    def RGBchange(self):
        if self.flag == False:
            self.imageValue = np.copy(self.imageStatus.getImage())
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
                    self.imageValue[self.imageValue[:, :, 0] >= self.redEnter.value()] = self.imageStatus.getColor()
                elif self.redOperation.currentText() == ">":
                    self.imageValue[self.imageValue[:, :, 0] <= self.redEnter.value()] = self.imageStatus.getColor()
                elif self.redOperation.currentText() == ">=":
                    self.imageValue[self.imageValue[:, :, 0] < self.redEnter.value()] = self.imageStatus.getColor()
                elif self.redOperation.currentText() == "<=":
                    self.imageValue[self.imageValue[:, :, 0] > self.redEnter.value()] = self.imageStatus.getColor()
                else:
                    self.imageValue[self.imageValue[:, :, 0] != self.redEnter.value()] = self.imageStatus.getColor()
                # process green
                if self.greenOperation.currentText() == "<":
                    self.imageValue[self.imageValue[:, :, 1] >= self.greenEnter.value()] = self.imageStatus.getColor()
                elif self.greenOperation.currentText() == ">":
                    self.imageValue[self.imageValue[:, :, 1] <= self.greenEnter.value()] = self.imageStatus.getColor()
                elif self.greenOperation.currentText() == ">=":
                    self.imageValue[self.imageValue[:, :, 1] < self.greenEnter.value()] = self.imageStatus.getColor()
                elif self.greenOperation.currentText() == "<=":
                    self.imageValue[self.imageValue[:, :, 1] > self.greenEnter.value()] = self.imageStatus.getColor()
                else:
                    self.imageValue[self.imageValue[:, :, 1] != self.greenEnter.value()] = self.imageStatus.getColor()
                # process blue
                if self.blueOperation.currentText() == "<":
                    self.imageValue[self.imageValue[:, :, 2] >= self.blueEnter.value()] = self.imageStatus.getColor()
                elif self.blueOperation.currentText() == ">":
                    self.imageValue[self.imageValue[:, :, 2] <= self.blueEnter.value()] = self.imageStatus.getColor()
                elif self.blueOperation.currentText() == ">=":
                    self.imageValue[self.imageValue[:, :, 2] < self.blueEnter.value()] = self.imageStatus.getColor()
                elif self.blueOperation.currentText() == "<=":
                    self.imageValue[self.imageValue[:, :, 2] > self.blueEnter.value()] = self.imageStatus.getColor()
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
                    self.imageStatus.addShanpshotImage(self.imageValue,True)
                    self.Flag = True
                    self.redEnter.setValue(0)
                    self.blueEnter.setValue(0)
                    self.greenEnter.setValue(0)
                    self.blueOperation.setCurrentIndex(0)
                    self.greenOperation.setCurrentIndex(0)
                    self.redOperation.setCurrentIndex(0)
                    self.Flag = False
                    self.colorButton.setStyleSheet("background-color: black");
                else:
                    self.imageStatus.addShanpshotImage(self.imageValue, False)
                    self.RGBchange()
                    self.imageStatus.removeDub()
            else:
                self.imageValue = misc.imread(fileName)
                self.imageStatus.addShanpshotImage(self.imageValue, False)
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
