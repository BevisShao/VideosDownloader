#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging


class NullHandler(logging.Handler):
    def emit(self, record): pass


class GlobalLogging:
    log = None
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    @staticmethod
    def getInstance(file_name):
        if GlobalLogging.log == None:
            GlobalLogging.log = GlobalLogging(file_name)
        return GlobalLogging.log

    def __init__(self, file_name):
        self.handler = None
        self.level = logging.INFO
        self.logger = logging.getLogger(file_name)
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        h = NullHandler()
        self.logger.addHandler(h)

    def setLoggingToFile(self, file):
        self.fh = logging.FileHandler(file)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def setLoggingToConsole(self):
        self.ch = logging.StreamHandler()
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)

    def setLoggingToHanlder(self, handler):
        self.handler = handler

    def setLoggingLevel(self, level):
        self.level = level
        self.logger.setLevel(level)

    def debug(self, s):
        self.logger.debug(s)
        if not self.handler == None and self.level <= logging.DEBUG:
            print(logging.DEBUG)
            print(self.level)
            self.handler('debug:' + s)

    def info(self, s):
        self.logger.info(s)
        if not self.handler == None and self.level <= logging.INFO:
            self.handler('info:' + s)

    def warn(self, s):
        self.logger.warn(s)
        if not self.handler == None and self.level <= logging.WARNING:
            self.handler('warn:' + s)

    def error(self, s):
        self.logger.error(s)
        if not self.handler == None and self.level <= logging.ERROR:
            self.handler('error:' + s)

    def critical(self, s):
        self.logger.critical(s)
        if not self.handler == None and self.level <= logging.CRITICAL:
            self.handler('critical:' + s)


