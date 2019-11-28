#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# #coding:utf-8

from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QGridLayout, QPushButton, QMessageBox, QTabWidget,
)
import sys
# sys.setdefaultencoding('utf-8')


class MyConsole(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent = parent

        self.initUI()

    # 初始化UI
    def initUI(self):
        self.gridlayout = QGridLayout()
        # 设置出20 x 20 的格局
        for i in range(20):
            self.gridlayout.setColumnStretch(i, 1)
            self.gridlayout.setRowStretch(i, 1)
        lb1 = QLabel(u'账户：')
        lb2 = QLabel(u'密码：')
        self.userEntry = QLineEdit()
        self.passEntry = QLineEdit()
        self.passEntry.setEchoMode(QLineEdit.Password)
        self.loginBtn = QPushButton(u"登录")
        self.loginBtn.setFixedSize(40, 20)
        self.loginBtn.clicked.connect(self.onLoginButton)
        # self.connect(self.loginBtn, QtCore.SIGNAL('clicked()'), self.onLoginButton)
        self.gridlayout.addWidget(lb1, 0, 0)
        self.gridlayout.addWidget(lb2, 1, 0)
        self.gridlayout.addWidget(self.userEntry, 0, 1, 1, 3)
        self.gridlayout.addWidget(self.passEntry, 1, 1, 1, 3)
        self.gridlayout.addWidget(self.loginBtn, 0, 4, 1, 2)
        self.setLayout(self.gridlayout)

        # 响应登录按钮
    def onLoginButton(self):
        username = self.userEntry.text()
        password = self.passEntry.text()
        QMessageBox.about(self, username + u'登录成功', u"密码是：" + password)
        # QTextCodec.setCodecForCStrings(QTextCodec.codecForName("utf-8"))
        print(username + u'登录成功！\n' + u"密码是：" + password)


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        tabs = QTabWidget(self)
        # tab1
        tab1 = QWidget()
        vbox = QVBoxLayout()
        console = MyConsole(self)
        vbox.addWidget(console)
        tab1.setLayout(vbox)
        # tab2
        self.tab2 = QTextEdit()
        tabs.addTab(tab1, u"控制台")
        tabs.addTab(self.tab2, u"日志输出")
        tabs.resize(500, 350)
        self.resize(500, 350)
        # 禁止最大化
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.show()
        # 重定向输出
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)
        # sys.stdout = EmittingStream(self.normalOutputWritten)
        # sys.stderr = EmittingStream()

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def normalOutputWritten(self, text):
        cursor = self.tab2.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.tab2.setTextCursor(cursor)
        self.tab2.ensureCursorVisible()


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

