#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QLabel, QGridLayout
                             ,QHBoxLayout, QVBoxLayout, QLineEdit, QTextEdit)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication


class Sample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
         1.Layout可以addLayout也可以addWidget，而窗口需要加载Widget，就需要先setLayout，通过Layout来间接添加；
         2.或者在Widget创建的时候绑定self： qbtn = QPushButton('Quit', self)
        :return:
        '''
        # qbtn = QPushButton(self)
        # # qbtn.setText('Quit')
        # qbtn.clicked.connect(QCoreApplication.instance().quit())
        # qbtn.resize(qbtn.sizeHint())
        # qbtn.move(50, 50)
        QToolTip.setFont(QFont('SansSerif', 10))                                # 设置字体
        # qbtn = QPushButton('Quit', self)
        qbtn = QPushButton('Quit')
        qbtn.clicked.connect(QCoreApplication.instance().quit)                  # 点击事件
        qbtn.resize(qbtn.sizeHint())
        # qbtn.setToolTip('点击退出')
        qbtn.setToolTip('<b>点击退出</b>')                                      # 设置鼠标悬停提示
        qbtn.move(50, 50)

        # 嵌套Layout
        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        # self.setLayout(vbox)

        # GridLayout
        grid = QGridLayout()
        # self.setLayout(grid)
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                '4', '5', '6', '*',
                 '1', '2', '3', '-',
                '0', '.', '=', '+']
        positions = [(i, j) for i in range(5) for j in range(4)]
        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)


        # GridLayout跨行、跨列
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')
        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()
        grid_2 = QGridLayout()
        grid_2.setSpacing(10)                       # 网格间距
        grid_2.addWidget(title, 1, 0)
        grid_2.addWidget(titleEdit, 1, 1)
        grid_2.addWidget(author, 2, 0)
        grid_2.addWidget(authorEdit, 2, 1)
        grid_2.addWidget(review, 3, 0)
        grid_2.addWidget(reviewEdit, 3, 1, 5, 1)     # 行、列、占用的行数、占用的列数
        self.setLayout(grid_2)


        self.move(300, 150)
        self.setWindowTitle('calculator')
        self.show()


        # self.setGeometry(300, 300, 250, 150)
        # self.setWindowTitle(r'This is Sample`s Tittle')
        # self.setWindowIcon(QIcon('favicon.ico'))
        # self.center()
        # self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', '确定退出？', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sm = Sample()
    sys.exit(app.exec_())
