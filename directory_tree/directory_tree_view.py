# encoding: utf-8
from lib import *

import platform
import model

import subprocess


class DirectoryTreeView(QTreeView):

    item_selected = Signal(str)

    def __init__(self, parent, root_paths=[]):
        widget.construct(self, parent)

        self.setModel(model.DirectoryTreeModel(root_paths))

        self.clicked.connect(lambda index: self.__on_selected_item(index))
        self.expanded.connect(lambda index: self.model().expand(index))

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__setup_context_menu)

    def __on_selected_item(self, index):
        item = self.model().itemFromIndex(index)
        self.item_selected.emit(item.path)

    def __setup_context_menu(self, point):

        def _open_directory(path):
            subprocess.call('"{}" "{}"'.format(platform.FILEOPEN_COMMAND, path), shell=True)

        menu_items = {
            u'フォルダを開く': lambda path: _open_directory(path),
        }

        menu = QMenu()
        for label in menu_items.keys():
            menu.addAction(label)

        executed_action = menu.exec_(self.mapToGlobal(point))
        action = menu_items[executed_action.text()]

        index = self.currentIndex()
        item = self.model().itemFromIndex(index)
        action(item.path)
