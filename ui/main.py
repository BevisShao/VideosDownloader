#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
from ui import MainUI
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QTextCodec
from tianxiantv import TianXianTV


class DownloadUI(MainUI.Ui_MainWindow, QMainWindow):
    def __init__(self, MainWindow):
        super().__init__(MainWindow)
        self.TianXianTV = TianXianTV()
        self.dirname = self.TianXianTV.config_parser.get('DOWNLOAD_PATH', 'BASE_PATH')
        self.start_url = self.TianXianTV.config_parser.get('DOWNLOAD_URL', 'URL')
        self.initUI(MainWindow)

    def initUI(self, MainWindow):
        self.setupUi(MainWindow)
        self.retranslateUi(MainWindow)
        if self.dirname:
            self.textEdit.setText(self.dirname)
        if self.start_url:
            self.textEdit_2.setText(self.start_url)
        MainWindow.show()
        self.pushButton_3.clicked.connect(self.show_FileDialog)
        self.pushButton.clicked.connect(self.start_download)
        # 重定向输出
        # sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        # sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)

    def show_FileDialog(self):
        self.dirname = QFileDialog.getExistingDirectory(self, 'Open file', '/home').strip()  # 选择目录
        self.textEdit.setText(self.dirname)
        self.TianXianTV.config_parser.set('DOWNLOAD_PATH', 'BASE_PATH', self.dirname)

    def start_download(self):
        self.start_url = self.textEdit_2.toPlainText()
        self.TianXianTV.config_parser.set('DOWNLOAD_URL', 'URL', self.start_url)
        self.start_tianxian()

    def start_tianxian(self):
        print('启动新线程...')
        self.TianXianTV.start()
        # self.TianXianTV.start_new_thread()

    def normalOutputWritten(self, text):
        cursor = self.textEdit_3.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textEdit_3.setTextCursor(cursor)
        self.textEdit_3.ensureCursorVisible()

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    # ui = MainUI.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # ui.pushButton_3.clicked.connect()
    # MainWindow.show()
    Download = DownloadUI(MainWindow)
    sys.exit(app.exec_())

