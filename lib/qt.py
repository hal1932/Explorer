# encoding: utf-8
from PySide.QtCore import *
from PySide.QtGui import *

import math


def add_widget(parent, cls, *args, **kwargs):
    if isinstance(parent, QWidget):
        instance = cls(parent, *args, **kwargs)
    else:
        instance = cls(parent.parentWidget(), *args, **kwargs)
    parent.addWidget(instance)
    return instance


def set_layout(parent, cls, *args, **kwargs):
    instance = cls(parent, *args, **kwargs)
    parent.setLayout(instance)
    return instance


def add_layout(parent, cls, *args, **kwargs):
    if isinstance(parent, QWidget):
        instance = cls(parent, *args, **kwargs)
    else:
        instance = cls(*args, **kwargs)
    parent.addLayout(instance)
    return instance


def get_file_icon(path):
    file_info = QFileInfo(path)
    return QFileIconProvider().icon(file_info)


def get_text_decoration(palette, state):
    if state & QStyle.State_Selected:
        pen = QPen(palette.color(QPalette.Active, QPalette.HighlightedText))
        brush = QBrush(palette.color(QPalette.Active, QPalette.Highlight))
    else:
        pen = QPen(palette.color(QPalette.Active, QPalette.Text))
        brush = None
    pen.setWidth(0)
    return pen, brush


def get_monocolor_decoration(color_name):
    color = QColor(color_name)
    brush = QBrush(color)
    pen = QPen(color)
    pen.setWidth(0)
    return pen, brush


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


def scale_size(rect, scale):
    return QSize(scale.width() * scale, scale.height() * scale)


def scale_rect(rect, scale):
    return QRect(
        rect.left() + rect.width() * (1.0 - scale) / 2.0,
        rect.top() + rect.height() * (1.0 - scale) / 2.0,
        rect.width() * scale,
        rect.height() * scale
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
        scale = float(cw) / tw
        tw = cw
        th *= scale

    if ch < th:
        scale = float(ch) / th
        th = ch
        tw *= scale

    return QSize(tw, th)
