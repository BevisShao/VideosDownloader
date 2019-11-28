#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QAction, QFileDialog,QMainWindow, QTextEdit, QLabel, QPushButton, QLineEdit, QVBoxLayout, QSizePolicy,
                             QInputDialog, QFontDialog, QApplication, QFrame, QColorDialog)
from PyQt5.QtGui import QColor, QFont, QIcon


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        col = QColor(0, 0, 0)
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)
        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.frm = QFrame(self)
        self.frm.setStyleSheet('QWidget { background-color: %s }' % col.name())
        self.frm.setGeometry(130, 22, 100, 100)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def showDialog(self):
        # text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        # if ok:
        #     self.le.setText(str(text))
        col = QColorDialog.getColor()
        if col.isValid():
            self.frm.setStyleSheet('QWidget {background-color: %s } ' % col.name())


class FontDialogSample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        btn = QPushButton('Dialog', self)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.move(20, 20)
        vbox.addWidget(btn)
        btn.clicked.connect(self.showDialog)
        self.lbl = QLabel('Knowledge only matters', self)
        self.lbl.move(130, 20)
        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Font dialog')
        self.show()

    def showDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)


class FileDialogSample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        openfile = QAction(QIcon('favicon.ico'), 'Open', self)
        openfile.setShortcut('Ctrl+O')
        openfile.setStatusTip('Open new file')
        openfile.triggered.connect(self.showDialog)
        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        filemenu.addAction(openfile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Font dialog')
        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')     # 选择文件
        if fname[0]:
            print('fname:{}-----fname[0]:{}'.format(fname, fname[0]))
            with open(fname[0], 'r', encoding='utf-8') as f:
                data = f.read()
                self.textEdit.setText(data)
        # dirname = QFileDialog.getExistingDirectory(self, 'Open file', '/home')  # 选择目录
        # self.textEdit.setText(dirname)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = Example()
    # ex = FontDialogSample()
    ex = FileDialogSample()
    sys.exit(app.exec_())


