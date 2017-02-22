# encoding: utf-8
from lib import *

import thumbnail_cache

import os


class FileListDelegate(QItemDelegate):

    def __init__(self):
        super(FileListDelegate, self).__init__()
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

        pen, brush = qt.get_text_decoration(option.palette, option.state)
        if brush is not None:
            painter.setBrush(brush)
            painter.drawRect(option.rect)
        painter.setPen(pen)
        painter.drawText(name_rect, Qt.AlignVCenter, name)
