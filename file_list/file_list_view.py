# encoding: utf-8
from lib import *

import platform

import model
import list_delegate
import thumbnail_delegate


class FileListView(QListView):

    open_requested = Signal(str)

    @property
    def count(self):
        return self.model().rowCount()

    @property
    def view_type(self):
        return self.__view_type

    def __init__(self, parent=None):
        widget.construct(self, parent)

        self.__view_type = None
        self.setModel(model.FileListModel())

        self.doubleClicked.connect(
            lambda index: self.open_requested.emit(index.data(Qt.EditRole))
        )

    def clear(self):
        self.model().clear()

    def set_directory(self, directory):
        self.clear()
        self.model().set_directory(directory)
        self.invalidate()

    def filter_items(self, needle):
        self.model().filter_items(needle)
        self.invalidate()

    def change_view(self, type_name):
        if self.__view_type == type_name:
            return

        if type_name == 'list':
            delegate = list_delegate.FileListDelegate()
            self.setItemDelegate(delegate)

            self.setViewMode(QListView.ListMode)
            self.setWrapping(False)
            self.setResizeMode(QListView.Fixed)
            self.setSpacing(1)
        elif type_name == 'thumbnail':
            delegate = thumbnail_delegate.FileThumbnailDelegate()
            delegate.set_thumbnail_length(100)
            self.setItemDelegate(delegate)

            self.setViewMode(QListView.IconMode)
            self.setWrapping(True)
            self.setResizeMode(QListView.Adjust)
            self.setSpacing(3)
        else:
            raise ValueError('invalid fileview type: {}'.format(type_name))

        self.__view_type = type_name

    def invalidate(self):
        m = self.model()
        self.setModel(None)
        self.setModel(m)
