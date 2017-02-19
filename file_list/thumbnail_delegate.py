# encoding: utf-8
from lib import *

import os
import threading
import Queue


class FileThumbnailDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(FileThumbnailDelegate, self).__init__(parent)
        self.__thumbnail_caches = {}

    def sizeHint(self, option, index):
        return QSize(100, 120)

    def paint(self, painter, option, index):
        path = index.data(Qt.DisplayRole)

        if path not in self.__thumbnail_caches:
            self.__thumbnail_caches[path] = _ThumbnailCache()

        image_rect = qt.resize_rect(option.rect, 100, 100)
        name_rect = QRect(option.rect.left(), option.rect.top() + 100, 100, 20)

        cache = self.__thumbnail_caches[path]
        if cache.pixmap is None:
            cache.load(path)

        if cache.pixmap is not None:
            painter.drawPixmap(image_rect, cache.pixmap)
        else:
            brush = QBrush(QColor('aliceblue'))
            painter.setBrush(brush)
            pen = QPen(brush.color())
            pen.setWidth(0)
            painter.setPen(pen)

            painter.drawRect(image_rect)

        painter.setPen(None)
        painter.drawText(name_rect, Qt.AlignCenter, os.path.basename(path))


class _ThumbnailCache(object):

    @property
    def pixmap(self):
        return self.__pixmap

    def __init__(self):
        _ThumbnailCache.__static_init__()
        self.__pixmap = None

    @staticmethod
    def __static_init__():
        if _ThumbnailCache.__initialized:
            return
        _ThumbnailCache.__directory_thumbnail = QPixmap('resources/Folder_64x.png')

    def load(self, path):
        if os.path.isdir(path):
            self.__pixmap = _ThumbnailCache.__directory_thumbnail
        elif os.path.splitext(path)[1].lower() in _ThumbnailCache.__image_exts:
            self.__pixmap = QPixmap(path)
        else:
            self.__pixmap = None

    __initialized = False
    __directory_thumbnail = None
    __image_exts = (u'.jpg', u'.png', u'.gif', u'.bmp')
