# encoding: utf-8
from lib import *

import model


class DirectoryTreeView(QTreeView):

    item_selected = Signal(str)

    def __init__(self, parent=None, root_paths=[]):
        super(DirectoryTreeView, self).__init__(parent)

        self.setModel(model.DirectoryTreeModel(root_paths=root_paths))

        self.clicked.connect(lambda index: self.__on_selected_item(index))
        self.expanded.connect(lambda index: self.model().expand(index))

    def __on_selected_item(self, index):
        item = self.model().itemFromIndex(index)
        self.item_selected.emit(item.path)
