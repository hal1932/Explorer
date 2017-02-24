# encoding: utf-8
from lib import *

import explorer_window

import sys


@entrypoint
def main():
    window = explorer_window.ExplorerWindow(directory='D:\\yuta\\Pictures\\ScreenShot')
    window.show()
    return window


if __name__ == '__main__':
    main()
