# encoding: utf-8
from lib import *

import os


class ThumbnailCache(object):

    def __init__(self):
        self.__itemsDic = {}

    def get_cached_pixmap(self, path):
        if path in self.__itemsDic:
            return self.__itemsDic[path]
        return None

    def load(self, path, size):
        if os.path.splitext(path)[1].lower() in ThumbnailCache.__image_exts:
            pixmap = QPixmap(path)
            pixmap_size = qt.fitting_scale_down(size, pixmap.size())
            pixmap = pixmap.scaled(pixmap_size)
        else:
            icon = qt.get_file_icon(path)
            size = icon.actualSize(size)
            pixmap = icon.pixmap(size)

        self.__itemsDic[path] = pixmap
        return pixmap

    __initialized = False
    __directory_thumbnail = None
    __image_exts = (u'.png', u'.jpg', u'.jpeg', u'.gif', u'.bmp')
