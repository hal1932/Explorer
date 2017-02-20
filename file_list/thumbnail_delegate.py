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
        return QSize(100, 130)

    def paint(self, painter, option, index):
        path = index.data(Qt.DisplayRole)

        if path not in self.__thumbnail_caches:
            self.__thumbnail_caches[path] = _ThumbnailCache(QSize(100, 100))

        cache = self.__thumbnail_caches[path]
        if cache.pixmap is None:
            cache.load(path)

        if cache.pixmap is not None:
            image_rect = qt.resize_rect(option.rect, cache.pixmap.size())
            image_rect = qt.center_rect(option.rect, image_rect)
            painter.drawPixmap(image_rect, cache.pixmap)
        else:
            brush = QBrush(QColor('aliceblue'))
            painter.setBrush(brush)
            pen = QPen(brush.color())
            pen.setWidth(0)
            painter.setPen(pen)

            image_rect = qt.resize_rect(option.rect, 100, 100)
            painter.drawRect(image_rect)

        name_rect = QRect(option.rect.left(), option.rect.top() + 100, 100, 30)
        painter.setPen(None)
        painter.drawText(name_rect, Qt.AlignCenter | Qt.AlignBottom, os.path.basename(path))


class _ThumbnailCache(object):

    @property
    def pixmap(self):
        return self.__pixmap

    def __init__(self, size):
        _ThumbnailCache.__static_init__(size)
        self.__pixmap = None

    @staticmethod
    def __static_init__(size):
        if _ThumbnailCache.__initialized:
            return
        _ThumbnailCache.__directory_thumbnail = QPixmap('resources/Folder_64x.png').scaled(size)
        _ThumbnailCache.__thumbnail_size = size

    def load(self, path):
        if os.path.isdir(path):
            self.__pixmap = _ThumbnailCache.__directory_thumbnail
        elif os.path.splitext(path)[1].lower() in _ThumbnailCache.__image_exts:
            pixmap = QPixmap(path)
            pixmap_size = qt.fitting_scale_down(pixmap.size(), _ThumbnailCache.__thumbnail_size)
            self.__pixmap = pixmap.scaled(pixmap_size)
        else:
            file_info = QFileInfo(path)
            icon = QFileIconProvider().icon(file_info)
            size = icon.actualSize(_ThumbnailCache.__thumbnail_size)
            self.__pixmap = icon.pixmap(size)

    __initialized = False
    __thumbnail_size = None
    __directory_thumbnail = None
    __image_exts = (u'.jpg', u'.png', u'.gif', u'.bmp')
