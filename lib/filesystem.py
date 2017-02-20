# encoding: utf-8
import sys
import os
import string
import glob


def list_drives():
    result = []

    if sys.platform == 'win32':
        for letter in string.ascii_uppercase:
            drive = '{}:{}'.format(letter, os.sep)
            if os.path.exists(drive):
                result.append(drive)
    else:
        result.append('/')

    return result


def has_directory(path):
    for path in glob.iglob(os.path.join(path, '*')):
        if os.path.isdir(path):
            return True
    return False


def list_directories(path, encoding=None):
    directories = []

    for path in glob.iglob(os.path.join(path, '*')):
        if encoding is not None:
            if not isinstance(path, unicode):
                path = path.decode(encoding)

        if os.path.isdir(path):
            directories.append(path)

    return directories


def list_directories_and_files(path, encoding=None):
    directories = []
    files = []

    for path in glob.iglob(os.path.join(path, '*')):
        if encoding is not None:
            if not isinstance(path, unicode):
                path = path.decode(encoding)

        if os.path.isdir(path):
            directories.append(path)
        else:
            files.append(path)

    return directories, files
