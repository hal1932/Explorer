# encoding: utf-8
from lib import *

import file_list

import exceptions
import glob
import os
import functools


class ExplorerWindow(QMainWindow):

    def __init__(self, parent=None, directory=None):
        super(ExplorerWindow, self).__init__(parent)
        self.__setup_ui()

        self.__history = []
        self.__current_history_index = -1

        self.__back_button.setEnabled(False)
        self.__forward_button.setEnabled(False)

        if directory is not None:
            self.change_directory(directory)

    def change_directory(self, directory):
        directory = os.path.abspath(directory)

        if not os.path.isdir(directory):
            raise exceptions.IOError(directory)

        if len(self.__history) > 0:
            if directory == self.__history[self.__current_history_index]:
                return

        if self.__current_history_index < len(self.__history) - 1:
            self.__history = self.__history[:self.__current_history_index]

        self.__history.append(directory)
        self.__current_history_index += 1

        self.__update_view()

    def __setup_ui(self):
        self.resize(800, 600)

        self.__setup_menu()

        root_widget = QWidget()
        self.setCentralWidget(root_widget)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignTop)
        root_layout.setContentsMargins(5, 5, 5, 5)
        root_widget.setLayout(root_layout)

        # operation menu
        operation_layout = QHBoxLayout()
        root_layout.addLayout(operation_layout)

        back_button = image_button.ImageButton('resources/Backward_32x.png')
        back_button.clicked.connect(self.__go_backward)

        forward_button = image_button.ImageButton('resources/Forward_32x.png')
        forward_button.clicked.connect(self.__go_forward)

        address_text = QLineEdit()
        address_text.setMinimumWidth(200)
        address_text.returnPressed.connect(
            lambda: self.change_directory(address_text.text())
            # functools.partial(self.change_directory, address_text.text())
        )

        search_text = QLineEdit()
        search_text.setMaximumWidth(200)

        operation_layout.addWidget(back_button)
        operation_layout.addWidget(forward_button)
        operation_layout.addWidget(address_text)
        operation_layout.addWidget(search_text)

        # file view
        splitter = QSplitter(Qt.Horizontal)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        root_layout.addWidget(splitter)

        directory_tree = QTreeView()
        directory_tree.setMaximumWidth(200)
        splitter.addWidget(directory_tree)

        fileitem_list = file_list.FileListView()
        fileitem_list.setMinimumWidth(200)
        splitter.addWidget(fileitem_list)

        # status bar
        status_layout = QHBoxLayout()
        root_layout.addLayout(status_layout)

        status_layout.addWidget(QPushButton())

        self.__back_button = back_button
        self.__forward_button = forward_button
        self.__address_text = address_text
        self.__file_list = fileitem_list

    def __setup_menu(self):
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        file_menu = QMenu('file', self)
        menu_bar.addMenu(file_menu)

        file_test_menu = QMenu('test', file_menu)
        file_menu.addMenu(file_test_menu)

    def __go_backward(self):
        self.__current_history_index -= 1
        self.__update_view()

    def __go_forward(self):
        self.__current_history_index += 1
        self.__update_view()

    def __update_view(self):
        directory = self.__history[self.__current_history_index]

        self.__file_list.clear()
        for entry in glob.iglob(os.path.join(directory, '*')):
            self.__file_list.add_item(entry)
        self.__file_list.invalidate()

        enable_backward = self.__current_history_index > 0
        self.__back_button.setEnabled(enable_backward)

        enable_forward = self.__current_history_index < len(self.__history) - 1
        self.__forward_button.setEnabled(enable_forward)

        self.__address_text.setText(directory)
