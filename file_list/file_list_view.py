# encoding: utf-8
from lib import *

import model
import delegate


class FileListView(QListView):

    @property
    def count(self):
        return self.model().rowCount()

    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)

        self.setModel(model.FileListModel())
        self.setItemDelegate(delegate.FileItemDelegate())

    def clear(self):
        self.model().clear()

    def add_item(self, item):
        self.model().add_item(item)

    def change_view(self, type_name):
        print(type_name)

    def invalidate(self):
        m = self.model()
        self.setModel(None)
        self.setModel(m)
