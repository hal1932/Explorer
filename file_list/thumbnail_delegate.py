# encoding: utf-8
from lib import *

import thumbnail_cache

import os
import threading
import Queue


class FileThumbnailDelegate(QItemDelegate):

    request_repainting = Signal()

    def __init__(self):
        super(FileThumbnailDelegate, self).__init__()

        self.__thumbnail_cache = thumbnail_cache.ThumbnailCache(False)
        # self.__thumbnail_cache = thumbnail_cache.ThumbnailCache(True)
        self.__thumbnail_cache.load_item_async.connect(self.request_repainting)

        self.__thumbnail_size = None
        self.__container_size = None
        self.set_thumbnail_length(100)

    def set_thumbnail_length(self, edge_length):
        self.__thumbnail_size = QSize(edge_length - 3, edge_length - 3)
        self.__container_size = QSize(edge_length, edge_length + 30)

    def sizeHint(self, option, index):
        return self.__container_size

    def paint(self, painter, option, index):
        name = index.data(Qt.DisplayRole)
        path = index.data(Qt.EditRole)

        pixmap = self.__thumbnail_cache.get_cached_pixmap(path)
        if pixmap is None:
            pixmap = self.__thumbnail_cache.load(path, self.__thumbnail_size)
            # self.__thumbnail_cache.load_async(path, self.__thumbnail_size)

        pen, brush = qt.get_text_decoration(option.palette, option.state)
        if brush is not None:
            painter.setPen(pen)
            painter.setBrush(brush)
            image_rect = qt.center_rect(option.rect, option.rect)
            painter.drawRect(image_rect)

        if pixmap is not None:
            image_rect = qt.resize_rect(option.rect, pixmap.size())
            image_rect = qt.center_rect(option.rect, image_rect)
            painter.drawPixmap(image_rect, pixmap)
        else:
            tmp_pen, tmp_brush = qt.get_monocolor_decoration('aliceblue')
            painter.setBrush(tmp_brush)
            painter.setPen(tmp_pen)

            image_rect = qt.resize_rect(option.rect, self.__thumbnail_size)
            image_rect = qt.center_rect(option.rect, image_rect)
            painter.drawRect(image_rect)

        name_rect = QRect(
            option.rect.left(), option.rect.top() + self.__thumbnail_size.height(),
            self.__container_size.width(), 30)
        painter.setPen(pen)
        painter.drawText(name_rect, Qt.AlignCenter | Qt.AlignBottom, name)
