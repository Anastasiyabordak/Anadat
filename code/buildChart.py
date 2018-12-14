import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
import numpy as np

class buildChart(QtWidgets.QMainWindow):

    def __init__(self, mainWindow, xData, yData):
        super().__init__()
        #self.charts = ['Histogram', '<=', '=', '<', '>']
        self.mainWindow = mainWindow
        print(xData)
        self.xData = xData
        self.yData = yData
        self.initUI()

    def initUI(self):
        uic.loadUi("GUI/chart.ui", self)
        plt.plot(self.xData[0], self.yData[0], 'r--')
        plt.savefig('graphs.png')
        self.image.setPixmap(QtGui.QPixmap("graphs.png"))
        #self.typeBox.addItems(self.charts)
        self.backButton.clicked.connect(self.showMainWindow)
        self.saveButton.clicked.connect(self.saveChart)
        self.show()
        self.setFixedSize(882, 687)

    def saveChart(self):
        fileName, _ = QFileDialog.getSaveFileName()
        self.plt.savefig(fileName)
    # Back to main
    def showMainWindow(self):
        global main_ui
        self.mainWindow.show()
        self.close()
