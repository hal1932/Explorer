# encoding: utf-8
from lib import *


class DirectoryTreeItemDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(DirectoryTreeItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        pass
