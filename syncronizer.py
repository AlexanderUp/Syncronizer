# encoding:utf-8
# Syncronizer project

import os

from pathlib import Path
from shutil import copyfile
from shutil import copytree
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
        self._missing_files_left_side = [] # files from LEFT missing in RIGHT
        self._missing_files_right_side = [] # files from RIGHT missing in LEFT
        self._altered_files_left_side = [] # files existing in LEFT and RIGHT simultaneously, but different by hash and in LEFT newer
        self._altered_files_right_side = [] # files existing in LEFT and RIGHT simultaneously, but different by hash and in RIGHT newer
        self.true_state = True
        self.strict = False

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

    def _get_state(self):
        # files from left side missing on right side
        self._missing_files_left_side = self.left_side.get_missing_files(self.right_side, true_path=self.true_state)
        # files from right side missing on left side
        self._missing_files_right_side = self.right_side.get_missing_files(self.left_side, true_path=self.true_state)
        # files present in both sides but different (if STRICT - by hash) and left_side newer
        self._altered_files_left_side = self.left_side.get_altered_files(self.right_side, true_path=self.true_state, strict=self.strict)
        # files present in both sides but different (if STRICT - by hash) and right_side newer
        self._altered_files_right_side = self.right_side.get_altered_files(self.left_side, true_path=self.true_state, strict=self.strict)
        return None

    def _save_state(self):
        pass

    def _load_state(self):
        pass

    def _get_path(self, side, file):
        return file if self.true_state else side.path.joinpath(file)

    def report(self):
        self._get_state()
        logger.info('****** Following files will be copied from LEFT to RIGHT:')
        for file in self._missing_files_left_side:
            logger.info(f'Missing: {self._get_path(self.left_side, file)}')

        for file in self._altered_files_left_side:
            logger.info(f'Altered: {self._get_path(self.left_side, file)}')

        logger.info('****** Following files will be copied from RIGHT to LEFT:')
        for file in self._missing_files_right_side:
            logger.info(f'Missing: {self._get_path(self.right_side, file)}')

        for file in self._altered_files_right_side:
            logger.info(f'Altered: {self._get_path(self.right_side, file)}')
        return None

    def syncronize(self):
        for file in self._missing_files_left_side:
            logger.info(f'Copy missing from <{self.left_side.path.name}> to <{self.right_side.path.name}>: {self.left_side.get_file_relative_path(file)}')
            self._copy_file(file, self.left_side, self.right_side)

        for file in self._missing_files_right_side:
            logger.info(f'Copy missing from <{self.right_side.path.name}> to <{self.left_side.path.name}>: {self.right_side.get_file_relative_path(file)}')
            self._copy_file(file, self.right_side, self.left_side)

        for file in self._altered_files_left_side:
            logger.info(f'Copy altered from <{self.left_side.path.name}> to <{self.right_side.path.name}>: {self.left_side.get_file_relative_path(file)}')
            self._copy_file(file, self.left_side, self.right_side)

        for file in self._altered_files_right_side:
            logger.info(f'Copy altered from <{self.right_side.path.name}> to <{self.left_side.path.name}>: {self.right_side.get_file_relative_path(file)}')
            self._copy_file(file, self.right_side, self.left_side)
        return None

    def _copy_file(self, file, src_side, dst_side,):
        rel_path = src_side.get_file_relative_path(file)
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
                logger.exception(err.filename)
            except SameFileError as err:
                logger.exception(err)
                logger.exception(err.filename)
            except FileNotFoundError as err:
                logger.exception(err)
                logger.exception(err.filename)
            else:
                logger.info(f'File {file} copied!')
        return None
