# encoding: utf-8
from lib import *

import file_list

import exceptions
import glob
import os
import functools
import itertools


if sys.platform == 'win32':
    FILESYSTEM_ENCODING = 'shift-jis'
else:
    raise EnvironmentError('{} is not supported'.format(sys.platform))


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

        self.change_fileview_type('list')

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

    def change_fileview_type(self, type_name):
        if self.__file_list.view_type == type_name:
            return

        button = next(
            itertools.ifilter(
                lambda x: x.arguments['type'] == type_name,
                self.__file_view_switcher.buttons()),
            None)
        if not button.isDown():
            button.setChecked(True)

        self.__file_list.change_view(type_name)

    def __setup_ui(self):
        self.resize(800, 600)

        self.__setup_menu()

        root_widget = QWidget()
        self.setCentralWidget(root_widget)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignTop)
        root_layout.setSpacing(3)
        root_widget.setLayout(root_layout)

        # operation menu
        operation_layout = QHBoxLayout()
        root_layout.addLayout(operation_layout)

        # back button
        back_button = image_widget.ImageButton('resources/Backward_32x.png')
        back_button.clicked.connect(self.__go_backward)
        operation_layout.addWidget(back_button)

        # forward button
        forward_button = image_widget.ImageButton('resources/Forward_32x.png')
        forward_button.clicked.connect(self.__go_forward)
        operation_layout.addWidget(forward_button)

        # address bar
        address_layout = QHBoxLayout()
        address_layout.setSpacing(0)
        operation_layout.addLayout(address_layout)

        address_icon = image_widget.ImageLabel('resources/Folder_16x.png')
        address_icon.setMargin(3)
        address_layout.addWidget(address_icon)

        address_text = QLineEdit()
        address_text.setMinimumWidth(200)
        address_text.returnPressed.connect(
            lambda: self.change_directory(address_text.text())
            # functools.partial(self.change_directory, address_text.text())
        )
        address_layout.addWidget(address_text)

        # file view switcher
        view_switcher_layout = QHBoxLayout()
        operation_layout.addLayout(view_switcher_layout)

        view_switcher = QButtonGroup()
        view_switcher.setExclusive(True)
        view_switcher.buttonClicked.connect(
            lambda x: self.change_fileview_type(x.arguments['type'])
        )

        file_view_types = {
            'list': 'resources/ListBox_24x.png',
            'thumbnail': 'resources/Image_32x.png',
        }
        for type_name, image_path in file_view_types.items():
            button = image_widget.ImageButton(image_path)
            button.setCheckable(True)
            button.arguments = {'type': type_name}

            view_switcher.addButton(button)
            view_switcher_layout.addWidget(button)

        # search filter
        search_layout = QHBoxLayout()
        search_layout.setSpacing(0)
        search_layout.setContentsMargins(0, 0, 0, 0)
        operation_layout.addLayout(search_layout)

        search_text = QLineEdit()
        search_text.setMaximumWidth(200)
        search_layout.addWidget(search_text)

        search_icon = image_widget.ImageLabel('resources/Search_16x.png')
        search_icon.setMargin(3)
        search_layout.addWidget(search_icon)

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

        status_text = QLabel()
        status_layout.addWidget(status_text)

        self.__back_button = back_button
        self.__forward_button = forward_button
        self.__address_text = address_text
        self.__file_list = fileitem_list
        self.__status_text = status_text
        self.__file_view_switcher = view_switcher

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
            self.__file_list.add_item(entry.decode(FILESYSTEM_ENCODING))
        self.__file_list.invalidate()

        enable_backward = self.__current_history_index > 0
        self.__back_button.setEnabled(enable_backward)

        enable_forward = self.__current_history_index < len(self.__history) - 1
        self.__forward_button.setEnabled(enable_forward)

        self.__address_text.setText(directory)

        self.__status_text.setText(u'{}個の項目'.format(self.__file_list.count))
