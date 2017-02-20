# encoding: utf-8
from lib import *

import file_list
import directory_tree
import explorer_window_model


class ExplorerWindow(QMainWindow):

    def __init__(self, parent=None, directory=None):
        super(ExplorerWindow, self).__init__(parent)

        self.__model = explorer_window_model.ExplorerWindowModel()
        self.__setup_ui()

        self.__model.directory_changed.connect(self.__update_view)
        self.__model.enable_backward_changed.connect(lambda enabled: self.__back_button.setEnabled(enabled))
        self.__model.enable_forward_changed.connect(lambda enabled: self.__forward_button.setEnabled(enabled))
        self.__model.enable_up_changed.connect(lambda enabled: self.__up_button.setEnabled(enabled))

        self.__back_button.setEnabled(False)
        self.__forward_button.setEnabled(False)

        self.change_fileview_type('list')

        self.__model.change_directory(directory)

    def change_fileview_type(self, type_name):
        if self.__file_list.view_type == type_name:
            return

        button = sequence.find(
            self.__file_view_switcher.buttons(),
            lambda x: x.arguments['type'] == type_name
        )
        assert(button is not None)

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
        back_button.clicked.connect(self.__model.go_backward)
        operation_layout.addWidget(back_button)

        # forward button
        forward_button = image_widget.ImageButton('resources/Forward_32x.png')
        forward_button.clicked.connect(self.__model.go_forward)
        operation_layout.addWidget(forward_button)

        # go up button
        up_button = image_widget.ImageButton('resources/Upload_32x.png')
        up_button.clicked.connect(self.__model.go_up)
        operation_layout.addWidget(up_button)

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
            lambda: self.__model.change_directory(address_text.text())
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
        search_text.returnPressed.connect(
            lambda: self.__file_list.filter_items(search_text.text())
        )
        search_layout.addWidget(search_text)

        search_icon = image_widget.ImageLabel('resources/Search_16x.png')
        search_icon.setMargin(3)
        search_layout.addWidget(search_icon)

        # file view
        splitter = QSplitter(Qt.Horizontal)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        root_layout.addWidget(splitter)

        dirtree_view = directory_tree.DirectoryTreeView(root_paths=filesystem.list_drives())
        dirtree_view.item_selected.connect(self.__model.change_directory)
        splitter.addWidget(dirtree_view)

        fileitem_list = file_list.FileListView()
        fileitem_list.open_requested.connect(self.__model.select_path)
        splitter.addWidget(fileitem_list)

        w = self.width()
        splitter.setSizes([w / 3 * 1, w / 3 * 2])

        # status bar
        status_layout = QHBoxLayout()
        root_layout.addLayout(status_layout)

        status_text = QLabel()
        status_layout.addWidget(status_text)

        self.__back_button = back_button
        self.__forward_button = forward_button
        self.__up_button = up_button
        self.__address_text = address_text
        self.__directory_tree = dirtree_view
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

    def __update_view(self):
        directory = self.__model.current_directory

        self.__file_list.set_directory(directory)
        self.__address_text.setText(directory)
        self.__status_text.setText(u'{}個の項目'.format(self.__file_list.count))
