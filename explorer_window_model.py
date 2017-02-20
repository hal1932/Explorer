# encoding: utf-8
from lib import *

import platform

import os
import exceptions
import subprocess


class ExplorerWindowModel(QObject):

    directory_changed = Signal(str)

    enable_backward_changed = Signal(bool)
    enable_forward_changed = Signal(bool)
    enable_up_changed = Signal(bool)

    @property
    def current_directory(self):
        if len(self.__history) == 0:
            return None
        return self.__history[self.__current_history_index]

    def __init__(self, parent=None):
        super(ExplorerWindowModel, self).__init__(parent)

        self.__history = []
        self.__current_history_index = -1

    def go_backward(self):
        self.__current_history_index -= 1

        self.directory_changed.emit(self.current_directory)
        self.__on_history_changed()

    def go_forward(self):
        self.__current_history_index += 1

        self.directory_changed.emit(self.current_directory)
        self.__on_history_changed()

    def go_up(self):
        current_path = self.__history[self.__current_history_index]
        parent_path = os.path.dirname(current_path)
        if current_path != parent_path:
            self.change_directory(parent_path)

    def change_directory(self, directory):
        if directory is None:
            return

        directory = os.path.abspath(directory)

        if not os.path.isdir(directory):
            raise exceptions.IOError(directory)

        if len(self.__history) > 0:
            if directory == self.__history[self.__current_history_index]:
                return

        if self.__current_history_index < len(self.__history) - 1:
            self.__history = self.__history[:self.__current_history_index + 1]
            self.__current_history_index = len(self.__history) - 1

        self.__history.append(directory)
        self.__current_history_index += 1

        self.directory_changed.emit(directory)
        self.__on_history_changed()

    def select_path(self, path):
        if os.path.isdir(path):
            self.change_directory(path)
        else:
            subprocess.call('"{}" "{}"'.format(platform.FILEOPEN_COMMAND, path), shell=True)

    def __can_go_up(self):
        current_path = self.__history[self.__current_history_index]
        parent_path = os.path.dirname(current_path)
        return current_path != parent_path

    def __on_history_changed(self):
        self.enable_backward_changed.emit(self.__current_history_index > 0)
        self.enable_forward_changed.emit(self.__current_history_index < len(self.__history) - 1)
        self.enable_up_changed.emit(self.__can_go_up())
