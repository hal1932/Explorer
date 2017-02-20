# encoding: utf-8
from lib import *

import os


class FileListDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(FileListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        item = index.data(Qt.DisplayRole)

        image_rect = qt.resize_rect(option.rect, QSize(16, 16))
        name_rect = qt.move_rect(option.rect, QPoint(16, 0))

        if os.path.isdir(item):
            thumbnail_path = 'resources/Folder_16x.png'
        else:
            thumbnail_path = 'resources/FileSystemEditor_16x.png'
        pixmap = QPixmap(thumbnail_path)
        painter.drawPixmap(image_rect, pixmap)

        palette = option.palette
        if option.state & QStyle.State_Selected:
            foreground_color = palette.color(QPalette.Active, QPalette.HighlightedText)
            background_color = palette.color(QPalette.Active, QPalette.Highlight)
        else:
            foreground_color = palette.color(QPalette.Active, QPalette.Text)
            background_color = None

        if background_color is not None:
            painter.setBrush(QBrush(background_color))
            painter.drawRect(option.rect)

        pen = QPen(foreground_color)
        pen.setWidth(0)
        painter.setPen(pen)
        painter.drawText(name_rect, Qt.AlignVCenter, item)
