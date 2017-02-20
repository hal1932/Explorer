# encoding: utf-8
from lib import *

import thumbnail_cache

import os


class FileListDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(FileListDelegate, self).__init__(parent)
        self.__thumbnail_size = QSize(16, 16)
        self.__thumbnail_cache = thumbnail_cache.ThumbnailCache()

    def paint(self, painter, option, index):
        name = index.data(Qt.DisplayRole)
        path = index.data(Qt.EditRole)

        image_rect = qt.resize_rect(option.rect, self.__thumbnail_size)
        name_rect = qt.move_rect(option.rect, QPoint(self.__thumbnail_size.width(), 0))

        pixmap = self.__thumbnail_cache.get_cached_pixmap(path)
        if pixmap is None:
            pixmap = self.__thumbnail_cache.load(path, self.__thumbnail_size)

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
        painter.drawText(name_rect, Qt.AlignVCenter, name)
