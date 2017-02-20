# encoding: utf-8
from lib import *

import platform

import os


class DirectoryTreeItem(QStandardItem):

    @property
    def path(self):
        return self.__path

    @property
    def name(self):
        name = os.path.basename(self.path)
        if len(name) == 0:
            name = self.path
        return name

    def __init__(self, parent=None, path=None):
        super(DirectoryTreeItem, self).__init__(parent)
        self.__path = path
        self.setEditable(False)

        if filesystem.has_directory(path):
            self.appendRow(None)

    def expand(self):
        self.removeRows(0, self.rowCount())

        children = filesystem.list_directories(self.path, platform.FILESYSTEM_ENCODING)
        self.appendRows([DirectoryTreeItem(path=path) for path in children])


class DirectoryTreeModel(QStandardItemModel):

    def __init__(self, parent=None, root_paths=[]):
        super(DirectoryTreeModel, self).__init__(parent)

        children = [DirectoryTreeItem(path=path) for path in root_paths]
        self.invisibleRootItem().appendRows(children)

    def data(self, index, role=Qt.DisplayRole):
        item = self.itemFromIndex(index)
        if role == Qt.DisplayRole:
            return item.name

    def columnCount(self, *args, **kwargs):
        return 1

    def headerData(self, *args, **kwargs):
        return ''

    def expand(self, index):
        item = self.itemFromIndex(index)
        item.expand()
