# encoding: utf-8
from PySide.QtGui import *


class ImageButton(QPushButton):

    def __init__(self, path, size=None, parent=None):
        super(ImageButton, self).__init__(parent)

        pix = QPixmap(path)
        icon = QIcon(pix)
        self.setIcon(icon)

        if size is not None:
            self.setIconSize(size)
