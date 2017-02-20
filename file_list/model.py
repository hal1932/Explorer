# encoding: utf-8
from lib import *

import platform

import os


class FileListModel(QAbstractListModel):

    def __init__(self, parent=None):
        super(FileListModel, self).__init__(parent)

        self.__base_items = None
        self.__items = None
        self.__needle = ''

        self.clear()

    def rowCount(self, parent=None):
        return len(self.__items)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if index.row() < 0 or len(self.__items) <= index.row():
            return None

        if role == Qt.DisplayRole:
            return os.path.basename(self.__items[index.row()])
        elif role == Qt.EditRole:
            return self.__items[index.row()]

        return None

    def clear(self):
        self.__base_items = []
        self.__items = []

    def set_directory(self, directory):
        directories, files = filesystem.list_directories_and_files(
            directory,
            platform.FILESYSTEM_ENCODING)

        self.__base_items.extend(directories)
        self.__base_items.extend(files)
        self.__execute_filter()

    def filter_items(self, needle):
        needle = needle.strip()
        self.__execute_filter(needle)

    def __execute_filter(self, needle=None):
        if needle is None:
            needle = self.__needle
        needle = needle.lower()

        if len(needle) > 0:
            self.__items = filter(lambda path: needle in path.lower(), self.__base_items)
        else:
            self.__items = self.__base_items

        self.__needle = needle



