# encoding: utf-8
from __future__ import print_function

import qt
import image_widget

from PySide.QtCore import *
from PySide.QtGui import *

import sys


def entrypoint(main):

    def _call_main(_main):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        widget = _main()

        sys.exit(app.exec_())

    return _call_main(main)
