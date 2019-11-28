#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp
from PyQt5.QtGui import QIcon


class Sample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        # 状态栏
        # self.statusBar().showMessage('Ready')       # 状态栏，竟然在界面左下方
        # 菜单栏
        exitAction = QAction(QIcon('favicon.ico'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        # exitAction.clicked.connect(qApp.quit)       # 无clicked操作
        self.statusBar()                              # Tip是显示在statusBar上的
        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        filemenu.addAction(exitAction)
        # 工具栏
        exitAction_tools = QAction(QIcon('favicon_csdn.ico'), 'Exit', self)
        exitAction_tools.setShortcut('Ctrl+P')
        exitAction_tools.triggered.connect(qApp.quit)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction_tools)

        self.setGeometry(300, 300, 250, 150)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Sample()
    sys.exit(app.exec_())
