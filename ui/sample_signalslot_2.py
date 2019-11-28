#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLCDNumber, QSlider, QVBoxLayout, QHBoxLayout, QApplication)


class Sample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        btn1 = QPushButton('BUT1', self)
        btn1.move(30, 50)
        btn2 =QPushButton('BUT2', self)
        btn2.move(150, 50)
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)
        self.statusBar()


        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Signal & slot')
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + 'was pressed')


class Communicate(QObject):
    closeAPP = pyqtSignal()


class Exapmle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.c = Communicate()
        self.c.closeAPP.connect(self.close)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.c.closeAPP.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = Sample()
    ex = Exapmle()
    sys.exit(app.exec_())

