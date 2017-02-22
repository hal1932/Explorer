# encoding: utf-8
from PySide.QtGui import *


def construct(self, parent):
    if isinstance(parent, QWidget):
        super(self.__class__, self).__init__(parent)
        parent.addWidget(self)
    elif isinstance(parent, QLayout):
        super(self.__class__, self).__init__()
        parent.addWidget(self)
    else:
        super(self.__class__, self).__init__()


class ImageButton(QPushButton):

    def __init__(self, parent, path, clicked):
        construct(self, parent)

        pix = QPixmap(path)
        icon = QIcon(pix)
        self.setIcon(icon)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        if clicked is not None:
            self.clicked.connect(clicked)


class ImageLabel(QLabel):

    def __init__(self, parent, path, size=None):
        construct(self, parent)

        pix = QPixmap(path)
        if size is not None:
            pix = pix.scaled(size)

        self.setPixmap(pix)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
