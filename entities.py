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

    def __eq__(self, other_file):
        '''Simplified equality test - only file names (base part of path) compared.'''
        # TODO: advanced comparison should be added - based on size, access/modification time
        # and as ultimative - based on file hash
        if not isinstance(other_file, File):
            raise TypeError('Can compare only <File> instances.')
        if self.name == other_file.name:
            return True
        return False

    def __repr__(self):
        return f'<File({self.path})>'

    def print_details(self):
        print(f'Path: {self.path}')
        print(f'Name: {self.name}')
        print(f'Created: {self.birthtime}')
        print(f'Last access: {self.access_time}')
        print(f'Last modification: {self.modification_time}')
        print(f'Last change: {self.change_time}')
        print(f'Size: {self.size}')
        print(f'Hash: {self.hash} ({self.hash_algo})')
        return None


class Folder():

    def __init__(self, path):
        self._path = None
        self._files = []
        self._update(path)

    @property
    def path(self):
        return self._path

    def __repr__(self):
        return f'<Folder({self.path})>'

    def __len__(self):
        return len(self._files)

    def __iter__(self):
        yield from self._files

    def __contains__(self, outer_file):
        for file in self:
            '''Simplified equality test'''
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
            relative_path = file.path.relative_to(self.path)
        except ValueError as err:
            logger.error(err)
            logger.error(f'!!!! Folder: {self.path}')
            logger.error(f'!!!! File: {file}')
        return relative_path

    def _is_exists(self, relative_path, other_folder):
        '''Check if file with specified relative path exists in another folder instance'''
        if other_folder.path.joinpath(relative_path).exists():
            return True
        return False

    def difference(self, other_folder):
        '''
        <diff_files> should contain files existing in both folder but in <self> files newer.
        Should be returned together with <missing_files>.
        '''
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


class Syncronizer():

    def __init__(self, left_side=None, right_side=None):
        self._left_side = left_side
        self._right_side = right_side
        self._missing_files_left_side = [] # files from LEFT missing in RIGHT
        self._missing_files_right_side = [] # files from RIGHT missing in LEFT
        self._different_files_left_side = [] # files existing in LEFT and RIGHT simultaneously, but in LEFT newer
        self._different_files_right_side = [] # files existing in LEFT and RIGHT simultaneously, but in RIGHT newer

    @property
    def left_side(self):
        return self._left_side

    @left_side.setter
    def left_side(self, folder):
        if isinstance(folder, Folder):
            self._left_side = folder

    @property
    def right_side(self):
        return self._right_side

    @right_side.setter
    def right_side(self, folder):
        if isinstance(folder, Folder):
            self._right_side = folder

    def __repr__(self):
        return f'<Syncronizer([{self.left_side}],[{self.right_side}])>'

    def add_left_side(self, left_side):
        if self.left_side:
            logger.warning('Left side already specified!')
        else:
            self.left_side = left_side
        return None

    def add_right_side(self, right_side):
        if self.right_side:
            logger.warning('Right side already specified!')
        else:
            self.right_side = right_side
        return None

    def _get_state(self):
        # files from left missing on right side
        self._missing_files_left_side = self.left_side.difference(self.right_side)
        # files from right missing on left side
        self._missing_files_right_side = self.right_side.difference(self.left_side)
        return None

    def report(self):
        '''Files to be copied L to R, R to L'''
        print('>> Following files will be copied from LEFT to RIGHT:')
        for file in self._missing_files_left_side:
            print(file)
        print('>> Following files will be copied from RIGHT to LEFT:')
        for file in self._missing_files_right_side:
            print(file)
        pass
