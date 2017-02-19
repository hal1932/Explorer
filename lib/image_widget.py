# encoding: utf-8
from PySide.QtGui import *


class ImageButton(QPushButton):

    def __init__(self, path, size=None, parent=None):
        super(ImageButton, self).__init__(parent)

        pix = QPixmap(path)
        if size is not None:
            pix = pix.scaled(size)

        icon = QIcon(pix)
        self.setIcon(icon)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


class ImageLabel(QLabel):

    def __init__(self, path, size=None, parent=None):
        super(ImageLabel, self).__init__()

        pix = QPixmap(path)
        if size is not None:
            pix = pix.scaled(size)

        self.setPixmap(pix)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
