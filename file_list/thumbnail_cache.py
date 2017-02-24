# encoding: utf-8
from lib import *

import cv2

import os
import threading
import Queue


class ThumbnailCache(QObject):

    load_item_async = Signal()

    def __init__(self, enable_load_async=False):
        super(ThumbnailCache, self).__init__()

        self.__items_dic = {}

        if enable_load_async:
            self.__load_queue = Queue.Queue()
            self.__items_lock = threading.Lock()
            self.__load_thread = threading.Thread(target=self.__load_async_impl)
            self.__load_thread.daemon = True
            self.__load_thread.start()

        self.__enable_async = enable_load_async

    def get_cached_pixmap(self, path):
        if self.__enable_async:
            with self.__items_lock:
                if path not in self.__items_dic:
                    return None
                image = self.__items_dic[path]

            if isinstance(image, QPixmap):
                return image

            height, width, dim = image.shape
            image = QImage(
                image.data,
                width, height, dim * width,
                QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)

            with self.__items_lock:
                self.__items_dic[path] = pixmap

            return pixmap
        else:
            if path not in self.__items_dic:
                return None
            return self.__items_dic[path]

    def load(self, path, size):
        if self.__enable_async:
            raise ValueError('load_sync is not enabled')

        if os.path.splitext(path)[1].lower() in ThumbnailCache.__image_exts:
            pixmap = QPixmap(path)
            pixmap_size = qt.fitting_scale_down(size, pixmap.size())
            pixmap = pixmap.scaled(pixmap_size)
        else:
            icon = qt.get_file_icon(path)
            size = icon.actualSize(size)
            pixmap = icon.pixmap(size)

        self.__items_dic[path] = pixmap
        return pixmap

    def load_async(self, path, size):
        if not self.__enable_async:
            raise ValueError('load_async is not enabled')

        if os.path.splitext(path)[1].lower() in ThumbnailCache.__image_exts:
            self.__load_queue.put((path, size))
        else:
            icon = qt.get_file_icon(path)
            size = icon.actualSize(size)
            pixmap = icon.pixmap(size)
            with self.__items_lock:
                self.__items_dic[path] = pixmap

    def __load_async_impl(self):
        while True:
            path, size = self.__load_queue.get()
            image = cv2.imread(path)
            height, width = image.shape[:2]
            if width != size.width() or height != size.height():
                size = qt.fitting_scale_down(size, QSize(width, height))
                image = cv2.resize(image, (size.width(), size.height()))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            with self.__items_lock:
                self.__items_dic[path] = image

            self.__load_queue.task_done()
            self.load_item_async.emit()
            print(path)

    __initialized = False
    __directory_thumbnail = None
    __image_exts = (u'.png', u'.jpg', u'.jpeg', u'.gif', u'.bmp')
