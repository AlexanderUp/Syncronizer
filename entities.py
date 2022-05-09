# encoding:utf-8
# Syncronizer project

import os

from pathlib import Path

from aux import get_hash
from app_logger import get_logger


logger = get_logger(__name__)


class File():

    def __init__(self, path):
        self._path = Path(path).expanduser()
        self._name = self.path.name
        self._birthtime = self.path.stat().st_birthtime
        self._access_time = self.path.stat().st_atime
        self._modification_time = self.path.stat().st_mtime
        self._change_time = self.path.stat().st_ctime
        self._size = self.path.stat().st_size
        self._hash_algo = None
        self._hash = None

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def birthtime(self):
        return self._birthtime

    @property
    def access_time(self):
        return self._access_time

    @property
    def modification_time(self):
        return self._modification_time

    @property
    def change_time(self):
        return self._change_time

    @property
    def size(self):
        return self._size

    @property
    def hash_algo(self):
        return self._hash_algo

    @property
    def hash(self):
        if not self._hash:
            self._hash_algo, self._hash = get_hash(self.path)
        return self._hash

    def show_details(self):
        print(f'Path: {self.path}')
        print(f'Name: {self.name}')
        print(f'Created: {self.birthtime}')
        print(f'Last access: {self.access_time}')
        print(f'Last modification: {self.modification_time}')
        print(f'Last change: {self.change_time}')
        print(f'Size: {self.size}')
        print(f'Hash: {self.hash} ({self.hash_algo})')
        return None

    def relative_to(self, folder):
        return self.path.relative_to(folder)

    def __eq__(self, other_file):
        '''Simplified equality test'''
        if not isinstance(other_file, File):
            raise TypeError('Can compare only <File> instances.')
        if self.name == other_file.name:
            return True
        return False

    def __repr__(self):
        return f'<File({self.path})>'


class Folder():

    def __init__(self, path):
        self._path = None
        self._files = []
        self._update(path)

    @property
    def path(self):
        return self._path

    def __len__(self):
        return len(self._files)

    def __iter__(self):
        yield from self._files

    def __contains__(self, outer_file):
        for file in self._files:
            if file == outer_file:
                return True
        return False

    def _update(self, path):
        logger.info(f'Updating... ({path})')
        self._path = Path(path)
        for dirpath, dirs, files in os.walk(path):
            for file in files:
                path_to_file = Path(dirpath) / file
                logger.debug(f'Adding: {path_to_file}')
                file_obj = File(path_to_file)
                self._files.append(file_obj)
        return None

    def _find_relative_path(self, file):
        try:
            relative_path = file.relative_to(self.path)
        except ValueError as err:
            logger.error(err)
            logger.error(f'Folder: {self.path}')
            logger.error(f'File: {file}')
        return relative_path

    def _is_exists(self, relative_path, other_folder):
        '''Check if file with specified relative path exists in another folder instance'''
        if other_folder.path.joinpath(relative_path).exists():
            return True
        return False

    def difference(self, other_folder):
        if self.path == other_folder.path:
            raise ValueError('Can not find difference with itself.')
        missing_files = []
        diff_files = []
        for file in self:
            relative_path = self._find_relative_path(file)
            if not self._is_exists(relative_path, other_folder):
                missing_files.append(file)
            else:
                # some additional checks for file identity required
                logger.debug(f'**{file} exists in {other_folder}')
                # print(f'same file: {file.hash == File(other_folder.path.joinpath(relative_path)).hash}')
        return missing_files

    def print_files(self):
        for file in self:
            print(file)
        return None

    def __repr__(self):
        return f'<Folder({self.path})>'


class Syncronizer():

    def __init__(self, folder_A=None, folder_B=None):
        self._folder_A = folder_A
        self._folder_B = folder_B
