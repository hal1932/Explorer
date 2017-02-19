# encoding: utf-8
from PySide.QtCore import *


def move_rect(rect, x, y):
    return QRect(
        x, y,
        rect.width(), rect.height()
    )


def resize_rect(rect, width, height):
    return QRect(
        rect.left(), rect.top(),
        width, height
    )
