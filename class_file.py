# encoding:utf-8
# Syncronizer project
# <File> entity
# <File> database model

from pathlib import Path
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import MetaData

from aux import get_hash

metadata = MetaData()

files_table = Table('files', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('path', String, nullable=False, unique=True),
                    Column('birthtime', Float, nullable=False),
                    Column('access_time', Float, nullable=False),
                    Column('modification_time', Float, nullable=False),
                    Column('change_time', Float, nullable=False),
                    Column('size', Integer, nullable=False),
                    Column('hash_algo', String, nullable=False),
                    Column('hash', String, nullable=False),
)


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
        '''
        If file will be changed after first hash calculation,
        hash will not be recalculated and hash value will not be updated.
        '''
        if not self._hash:
            self._hash_algo, self._hash = get_hash(self.path)
        return self._hash

    def __repr__(self):
        return f'<File({self.path})>'
