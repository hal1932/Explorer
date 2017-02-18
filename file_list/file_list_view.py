# encoding: utf-8
from lib import *

import model
import delegate


class FileListView(QListView):

    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)

        self.__items = []

        self.setModel(model.FileListModel())
        self.setItemDelegate(delegate.FileItemDelegate())

    def clear(self):
        self.model().clear()

    def add_item(self, item):
        self.model().add_item(item)

    def invalidate(self):
        m = self.model()
        self.setModel(None)
        self.setModel(m)
