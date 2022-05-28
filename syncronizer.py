# encoding:utf-8
# Syncronizer project

import os
import sqlalchemy
import config

from pathlib import Path
from shutil import copytree
from shutil import copyfile
from shutil import SameFileError
from shutil import ExecError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper

from class_file import File
from class_file import files_table
from class_file import metadata
from class_folder import Folder
from app_logger import get_logger


mapper(File, files_table, column_prefix='_')


conf = config.Config()
logger = get_logger(__name__)


class Syncronizer():

    def __init__(self, left_side=None, right_side=None):
        self._left_side = left_side
        self._right_side = right_side
        self._files_from_left_to_right = [] # files to be copied from LEFT to RIGHT
        self._files_from_right_to_left = [] # files to be copied from RIGHT to LEFT
        self._files_to_be_deleted_from_left = []
        self._files_to_be_deleted_from_right = []
        self.true_state = True
        self.strict = False
        if left_side:
            self.add_left_side(left_side)
        if right_side:
            self.add_right_side(right_side)

    def __repr__(self):
        return f'<Syncronizer([{self.left_side}], [{self.right_side}])>'

    @property
    def left_side(self):
        return self._left_side

    @property
    def right_side(self):
        return self._right_side

    def add_left_side(self, left_side):
        if self.left_side:
            logger.warning('Left side already specified!')
        elif isinstance(left_side, Folder):
            self._left_side = left_side
        return None

    def add_right_side(self, right_side):
        if self.right_side:
            logger.warning('Right side already specified!')
        elif isinstance(right_side, Folder):
            self._right_side = right_side
        return None

    def _is_equal_files(self, file, other_file):
        if self.strict and file.hash == other_file.hash:
            return True
        elif file.size == other_file.size:
            return True
        return False

    def _is_newer(self, file, other_file):
        return file.modificaton_time > other_file.modificaton_time

    def _get_file_relative_path(self, path_to_file, folder):
        '''Return relative part of path reffering to given path.'''
        return os.path.relpath(path_to_file, start=folder.path)

    def _get_path(self, folder, file):
        return file if self.true_state else os.path.join(folder.path, file)

    def _get_files_to_be_syncronized(self, folder, other_folder):
        if folder.path == other_folder.path:
            raise ValueError('Both sides are same!')

        files = []

        for file in folder:
            relative_path = self._get_file_relative_path(file.path, folder)
            other_file_path = os.path.join(other_folder.path, relative_path)
            if os.path.exists(other_file_path):
                other_file = other_folder.get_file_instance(other_file_path)
                if not other_file:
                    raise TypeError('Something went wrong with file entity retrieving.')
                if self._is_equal_files(file, other_file):
                    continue
                if not self.is_newer(file, other_file):
                    continue

            if self.true_state:
                files.append(file)
            else:
                files.append(relative_path)
        return files

    def _get_state(self):
        if not self.left_side and self.right_side:
            raise ValueError('Some side is not initiated!')
        if self.left_side.path == self.right_side.path:
            raise ValueError('Both sides are same!')
        # files to be copied from left to right
        self._files_from_left_to_right = self._get_files_to_be_syncronized(self.left_side, self.right_side)
        # files to be copied from right to left
        self._files_from_right_to_left = self._get_files_to_be_syncronized(self.right_side, self.left_side)
        return None

    def _copy_file(self, path_to_file, src_side, dst_side):
        rel_path = self._get_file_relative_path(path_to_file, src_side)
        dest_path = os.path.join(dst_side.path, rel_path)
        logger.debug(f'Destination: {dest_path}')

        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        except OSError as err:
            logger.exception(err)
        else:
            try:
                copyfile(path_to_file, dest_path)
            except SameFileError as err:
                logger.exception(err)
            except FileNotFoundError as err:
                logger.exception(err)
            except OSError as err:
                logger.exception(err)
            else:
                logger.info(f'Copied: {path_to_file}')
        return None

    def report(self):
        self._get_state()
        logger.info('****** Following files will be copied from LEFT to RIGHT:')
        for file in self._files_from_left_to_right:
            logger.info(f'{self._get_path(self.left_side, file)}')

        logger.info('****** Following files will be copied from RIGHT to LEFT:')
        for file in self._files_from_right_to_left:
            logger.info(f'{self._get_path(self.right_side, file)}')
        return None

    def syncronize(self):
        for file in self._files_from_left_to_right:
            logger.info(f'Copy from <{self.left_side.path}> to <{self.right_side.path}>: {self._get_file_relative_path(file.path, self.left_side)}')
            self._copy_file(file.path, self.left_side, self.right_side)

        for file in self._files_from_right_to_left:
            logger.info(f'Copy from <{self.right_side.path}> to <{self.left_side.path}>: {self._get_file_relative_path(file.path, self.right_side)}')
            self._copy_file(file.path, self.right_side, self.left_side)
        return None
