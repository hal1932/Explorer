# encoding: utf-8
from lib import *


class FileItemDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(FileItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        item = index.data(Qt.DisplayRole)

        palette = option.palette
        if option.state & QStyle.State_Selected:
            foreground_color = palette.color(QPalette.Active, QPalette.HighlightedText)
            background_color = palette.color(QPalette.Active, QPalette.Highlight)
        else:
            foreground_color = palette.color(QPalette.Active, QPalette.Text)
            background_color = None

        if background_color is not None:
            painter.setBrush(QBrush(background_color))
            painter.drawRect(option.rect)

        pen = QPen(foreground_color)
        pen.setWidth(0)
        painter.setPen(pen)
        painter.drawText(option.rect, Qt.AlignVCenter, item)
