# encoding:utf-8
# Syncronizer project
# <Folder> entity

import os
import config

from class_file import File
from class_file import files_table
from app_logger import get_logger


conf = config.Config()
logger = get_logger(__name__)


class Folder():

    def __init__(self, path=None):
        self._path = None
        self._files = []
        self._skip_hidden = True
        if path:
            self.update(path)

    def __repr__(self):
        return f'<Folder({self.path})>'

    def __len__(self):
        return len(self._files)

    def __iter__(self):
        yield from self._files

    def __contains__(self, file):
        for file_ in self:
            if file_.path == file.path:
                return True
        return False

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if not os.path.exists(path):
            raise ValueError('Given path does not exist!')
        self._path = path

    @property
    def skip_hidden(self):
        return self._skip_hidden

    @skip_hidden.setter
    def skip_hidden(self, value):
        if isinstance(value, bool):
            self._skip_hidden = value
        else:
            raise TypeError('Only boolean values permitted!')

    def update(self, path):
        if not path:
            raise ValueError('Can not update with empty path!')
        if self.path:
            raise ValueError('Folder already initiated!')

        logger.info(f'Updating... ({path})')
        self.path = path
        for dirpath, dirs, files in os.walk(path):
            for file in files:
                path_to_file = os.path.join(dirpath, file)

                if any((func(path_to_file) for func in conf.FILE_NAME_CHECK_FUNCS)):
                    logger.info(f'Skipped: {path_to_file}')
                    continue

                file_obj = File(path_to_file)
                self._files.append(file_obj)
                logger.debug(f'Add file: {file_obj}')
        return None

    def get_file_instance(self, path):
        # probably bottleneck in case of huge amount of file searches
        for file in self:
            if file.path == path:
                return file
        return None
