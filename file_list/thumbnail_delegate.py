# encoding: utf-8
from lib import *

import thumbnail_cache

import os
import threading
import Queue


class FileThumbnailDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(FileThumbnailDelegate, self).__init__(parent)

        self.__thumbnail_cache = thumbnail_cache.ThumbnailCache()

        self.__thumbnail_size = None
        self.__container_size = None
        self.set_thumbnail_length(100)

    def set_thumbnail_length(self, edge_length):
        self.__thumbnail_size = QSize(edge_length, edge_length)
        self.__container_size = QSize(edge_length, edge_length + 30)

    def sizeHint(self, option, index):
        return self.__container_size

    def paint(self, painter, option, index):
        name = index.data(Qt.DisplayRole)
        path = index.data(Qt.EditRole)

        pixmap = self.__thumbnail_cache.get_cached_pixmap(path)
        if pixmap is None:
            pixmap = self.__thumbnail_cache.load(path, self.__thumbnail_size)

        if pixmap is not None:
            image_rect = qt.resize_rect(option.rect, pixmap.size())
            image_rect = qt.center_rect(option.rect, image_rect)
            painter.drawPixmap(image_rect, pixmap)
        else:
            brush = QBrush(QColor('aliceblue'))
            painter.setBrush(brush)
            pen = QPen(brush.color())
            pen.setWidth(0)
            painter.setPen(pen)

            image_rect = qt.resize_rect(option.rect, self.__thumbnail_size)
            painter.drawRect(image_rect)

        name_rect = QRect(
            option.rect.left(), option.rect.top() + self.__thumbnail_size.height(),
            self.__container_size.width(), 30)
        painter.setPen(None)
        painter.drawText(name_rect, Qt.AlignCenter | Qt.AlignBottom, name)


