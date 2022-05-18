# encoding:utf-8
# Syncronizer project

import os

from pathlib import Path
from shutil import copytree
from shutil import copyfile
from shutil import SameFileError
from shutil import ExecError

from class_file import File
from class_folder import Folder
from app_logger import get_logger


logger = get_logger(__name__)


class Syncronizer():

    def __init__(self, left_side=None, right_side=None):
        self._left_side = left_side
        self._right_side = right_side
        self._files_from_left_to_right = [] # files to be copied from LEFT to RIGHT
        self._files_from_right_to_left = [] # files to be copied from RIGHT to LEFT
        self.true_state = True
        self.strict = False
        if left_side:
            self.add_left_side(left_side)
        if right_side:
            self.add_right_side(right_side)

    @property
    def left_side(self):
        return self._left_side

    @property
    def right_side(self):
        return self._right_side

    def __repr__(self):
        return f'<Syncronizer([{self.left_side}], [{self.right_side}])>'

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

    def get_file_relative_path(self, file, folder):
        '''Return relative part of file path reffering to given folder.'''
        return file.path.relative_to(folder.path)

    def is_file_exists(self, folder, relative_path):
        '''Check if file with specified relative path exists in given folder instance.'''
        if folder.path.joinpath(relative_path).exists():
            return True
        return False

    def is_equal_files(self, file, other_file):
        if self.strict and file.hash == other_file.hash:
            return True
        elif file.size == other_file.size:
            return True
        return False

    def is_newer(self, file, other_file):
        return file.modificaton_time > other_file.modificaton_time

    def get_file_to_be_syncronized(self, folder, other_folder):
        if folder.path == other_folder.path:
            raise ValueError('Both sides are same!')

        files = []

        for file in folder:
            relative_path = self.get_file_relative_path(file, folder)
            if self.is_file_exists(other_folder, relative_path):
                other_file_path = other_folder.path.joinpath(relative_path)
                other_file = other_folder.get_file_instance(other_file_path)

                if self.is_equal_files(file, other_file):
                    continue
                if not self.is_newer(file, other_file):
                    continue

            if self.true_state:
                files.append(file)
            else:
                files.append(relative_path)
        return files

    def get_deleted_files(self):
        pass

    def _get_state(self):
        if not self.left_side and self.right_side:
            raise ValueError('Some side is not initiated!')
        # files to be copied from left to right
        self._files_from_left_to_right = self.get_file_to_be_syncronized(self.left_side, self.right_side)
        # files to be copied from right to left
        self._files_from_right_to_left = self.get_file_to_be_syncronized(self.right_side, self.left_side)
        return None

    def _get_path(self, side, file):
        return file if self.true_state else side.path.joinpath(file)

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
            logger.info(f'Copy from <{self.left_side.path.name}> to <{self.right_side.path.name}>: {self.get_file_relative_path(file, self.left_side)}')
            self._copy_file(file, self.left_side, self.right_side)

        for file in self._files_from_right_to_left:
            logger.info(f'Copy from <{self.right_side.path.name}> to <{self.left_side.path.name}>: {self.get_file_relative_path(file, self.right_side)}')
            self._copy_file(file, self.right_side, self.left_side)
        return None

    def _copy_file(self, file, src_side, dst_side):
        rel_path = self.get_file_relative_path(file, src_side)
        dest_path = dst_side.path.joinpath(rel_path)
        logger.debug(f'Destination: {dest_path}')

        try:
            copytree(file.path.parent, dest_path.parent, dirs_exist_ok=True)
        except ExecError as err:
            logger.exception(err)
        else:
            try:
                copyfile(file.path, dest_path)
            except ExecError as err:
                logger.exception(err)
            except SameFileError as err:
                logger.exception(err)
            except FileNotFoundError as err:
                logger.exception(err)
            else:
                logger.info(f'Copied: {file}')
        return None

    def _save_state(self):
        pass

    def _load_state(self):
        pass
