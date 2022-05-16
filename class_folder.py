# encoding:utf-8
# Syncronizer project
# <Folder> entity

import os

from pathlib import Path

from class_file import File
from app_logger import get_logger


logger = get_logger(__name__)


class Folder():

    def __init__(self, path, skip_hidden=True):
        self._path = None
        self._files = []
        self._skip_hidden = skip_hidden
        self.update(path)

    @property
    def path(self):
        return self._path

    def __repr__(self):
        return f'<Folder({self.path})>'

    def __len__(self):
        return len(self._files)

    def __iter__(self):
        yield from self._files

    def update(self, path):
        if self.path:
            raise ValueError('Folder already initiated!')
        logger.info(f'Updating... ({path})')
        self._path = Path(path)
        for dirpath, dirs, files in os.walk(path):
            for file in files:
                path_to_file = Path(dirpath) / file
                if self._skip_hidden and path_to_file.stem.startswith('.'):
                    logger.debug(f'Skipped hidden <{path_to_file}>')
                    continue
                file_obj = File(path_to_file)
                self._files.append(file_obj)
                logger.debug(f'Added file: {file_obj}')
        return None

    def get_file_relative_path(self, file):
        return file.path.relative_to(self.path)

    def is_file_exists(self, relative_path):
        '''Check if file with specified relative path exists in folder instance'''
        if self.path.joinpath(relative_path).exists():
            return True
        return False

    def get_missing_files(self, other_folder, true_path=False):
        if self.path == other_folder.path:
            raise ValueError('Can not find difference (other side has the same path).')

        missing_files = []

        for file in self:
            relative_path = self.get_file_relative_path(file)
            if not other_folder.is_file_exists(relative_path):
                if true_path:
                    missing_files.append(file)
                else:
                    missing_files.append(relative_path)
        return missing_files

    def get_altered_files(self, other_folder, true_path=False, strict=False):
        '''
        <altered_files> should contain files existing in both folder but with different hash and files in <self> newer.
        '''
        if self.path == other_folder.path:
            raise ValueError('Can not find difference (other side has the same path).')

        altered_files = []

        for file in self:
            relative_path = self.get_file_relative_path(file)
            if other_folder.is_file_exists(relative_path):
                other_file = File(other_folder.path.joinpath(relative_path))
                if strict:
                    if file.hash == other_file.hash:
                        continue
                    elif file.modificaton_time < other_file.modification:
                        continue
                elif file.size == other_file.size:
                    continue
                elif file.modificaton_time < other_file.modificaton_time:
                    continue
                if true_path:
                    altered_files.append(file)
                else:
                    altered_files.append(relative_path)
        return altered_files
