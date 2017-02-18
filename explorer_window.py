# encoding: utf-8
import exceptions
import glob
import os

from lib import *
import file_list


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
        if not os.path.isdir(directory):
            raise exceptions.IOError(directory)

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

        search_text = QLineEdit()
        search_text.setMaximumWidth(200)

        operation_layout.addWidget(back_button)
        operation_layout.addWidget(forward_button)
        operation_layout.addWidget(address_text)
        operation_layout.addWidget(search_text)

        # file list
        self.__file_list = file_list.FileListView()
        root_layout.addWidget(self.__file_list)

        # status bar
        status_layout = QHBoxLayout()
        root_layout.addLayout(status_layout)

        status_layout.addWidget(QPushButton())

        self.__back_button = back_button
        self.__forward_button = forward_button

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

    def __update_history_button(self):
        print(self.__history, self.__current_history_index)

        enable_backword = self.__current_history_index > 0
        self.__back_button.setEnabled(enable_backword)

        enable_forward = self.__current_history_index < len(self.__history) - 1
        self.__forward_button.setEnabled(enable_forward)

    def __update_view(self):
        directory = self.__history[self.__current_history_index]

        self.__file_list.clear()
        for entry in glob.iglob(os.path.join(directory, '*')):
            #print(entry)
            self.__file_list.add_item(entry)

        self.__file_list.invalidate()
        self.__update_history_button()
