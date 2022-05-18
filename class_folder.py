# encoding:utf-8
# Syncronizer project
# <Folder> entity

import os

from pathlib import Path

from class_file import File
from app_logger import get_logger


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
    def path(self, value):
        if isinstance(value, Path):
            self._path = value
        else:
            raise TypeError('Path object needed!')

    @property
    def skip_hidden(self):
        return self._skip_hidden

    @skip_hidden.setter
    def skip_hidden(self, value):
        if isinstance(value, bool):
            self._skip_hidden = value
        else:
            raise TypeError('Only boolean valeus permitted!')

    def update(self, path):
        if not path:
            raise ValueError('Can not update with empty path!')
        if self.path:
            raise ValueError('Folder already initiated!')

        logger.info(f'Updating... ({path})')
        self.path = Path(path)
        for dirpath, dirs, files in os.walk(path):
            for file in files:
                path_to_file = Path(dirpath) / file
                if self._skip_hidden and path_to_file.stem.startswith('.'):
                    logger.debug(f'Skip hidden <{path_to_file}>')
                    continue
                file_obj = File(path_to_file)
                self._files.append(file_obj)
                logger.debug(f'Add file: {file_obj}')
        return None

    def get_file_instance(self, path: Path) -> File:
        # probably bottleneck in case of huge amount of file searches
        for file in self:
            if file.path == path:
                return file
        return None
