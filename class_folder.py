# encoding:utf-8
# Syncronizer project
# <Folder> entity

import os
import sqlalchemy

from pathlib import Path
from sqlalchemy.orm import mapper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from class_file import File
from class_file import files_table
from class_file import metadata
from app_logger import get_logger


logger = get_logger(__name__)

DB_NAME = '_files_db.sqlite'

# mapper(File, files_table, column_prefix='_')
mapper(File, files_table)


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
        self.session = self._create_session()
        for dirpath, dirs, files in os.walk(path):
            for file in files:
                path_to_file = Path(dirpath) / file
                if path_to_file.name == DB_NAME:
                    continue
                if self._skip_hidden and path_to_file.stem.startswith('.'):
                    logger.debug(f'Skip hidden <{path_to_file}>')
                    continue
                file_obj = File(path_to_file)
                self._files.append(file_obj)
                logger.debug(f'Add file: {file_obj}')

                # print(f'file.path: {file_obj.path}')
                # print(f'file._path: {file_obj._path}')
                # print(f'file.hash_algo: {file_obj.hash_algo}')

                self.session.add(file_obj)
                try:
                    # self.session.add(file_obj)
                    self.session.commit()
                except sqlalchemy.exc.SQLAlchemyError as err:
                    logger.error(f'{err}')
                    self.session.rollback()
                else:
                    logger.debug(f'Successfully commited: {file_obj}')
        self.session.close()
        return None

    def get_file_instance(self, path: Path) -> File:
        # probably bottleneck in case of huge amount of file searches
        for file in self:
            if file.path == path:
                return file
        return None

    def _create_session(self):
        path_to_db = self.path.joinpath(DB_NAME)
        engine = create_engine('sqlite:///' + path_to_db.as_posix())
        logger.info(f'DB engine: {engine}')
        metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        logger.debug(f'Session: {session}')
        return session
