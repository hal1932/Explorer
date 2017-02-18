# encoding: utf-8
from lib import *

import view
import model


class FileListView(QListView):

    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)
        self.__items = []
        self.__setup_ui()

    def clear(self):
        self.__items.clear()

    def add_item(self, item):
        self.__items.append(item)

    def __setup_ui(self):
        pass
