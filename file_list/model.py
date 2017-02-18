# encoding: utf-8
from lib import *


class FileListModel(QAbstractListModel):

    def __init__(self, parent=None):
        super(FileListModel, self).__init__(parent)

        self.__items = None

        self.clear()

    def rowCount(self, parent):
        return len(self.__items)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if index.row() < 0 or len(self.__items) <= index.row():
            return None

        if role == Qt.DisplayRole:
            return self.__items[index.row()]

        return None

    def clear(self):
        self.__items = []

    def add_item(self, item):
        self.__items.append(item)
