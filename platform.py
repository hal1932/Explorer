# encoding: utf-8
import sys


if sys.platform == 'win32':
    FILESYSTEM_ENCODING = 'shift-jis'
    FILEOPEN_COMMAND = 'explorer'
else:
    raise EnvironmentError('{} is not supported'.format(sys.platform))
