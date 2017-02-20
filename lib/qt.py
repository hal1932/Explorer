# encoding: utf-8
from PySide.QtCore import *
from PySide.QtGui import *

import math


def get_file_icon(path):
    file_info = QFileInfo(path)
    return QFileIconProvider().icon(file_info)


def move_rect(rect, position):
    return QRect(
        rect.x() + position.x(), rect.y() + position.y(),
        rect.width(), rect.height()
    )


def resize_rect(rect, size):
    return QRect(
        rect.left(), rect.top(),
        size.width(), size.height()
    )


def center_rect(container, target):
    cw, tw = container.width(), target.width()
    max_w, min_w = max(cw, tw), min(cw, tw)
    ofs_w = (max_w - min_w) / float(2)
    ofs_w = math.copysign(ofs_w, cw - tw)

    ch, th = container.height(), target.height()
    max_h, min_h = max(ch, th), min(ch, th)
    ofs_h = (max_h - min_h) / float(2)
    ofs_h = math.copysign(ofs_h, ch - th)

    return QRect(
        target.left() + ofs_w, target.top() + ofs_h,
        tw, th
    )


def fitting_scale_down(container, target):
    cw, tw = container.width(), target.width()
    ch, th = container.height(), target.height()

    if cw < tw:
        scale = (tw - cw) / float(tw)
        tw = cw
        th = ch * scale

    if ch < th:
        scale = (th - ch) / float(th)
        th = ch
        tw = cw * scale

    return QSize(tw, th)
