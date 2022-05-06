# encoding:utf-8
# Syncronizer project

import os

from aux import get_hash


class File():

    def __init__(self, path):
        self._path = path
        self._name = os.path.basename(path)
        self._creation_time = os.stat(path).st_birthtime
        self._access_time = os.path.getatime(path)
        self._modification_time = os.path.getmtime(path)
        self._change_time = os.path.getctime(path)
        self._size = os.path.getsize(path)
        self._hash = None

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def creation_time(self):
        return self._creation_time

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
    def hash(self):
        if not self._hash:
            self._hash = get_hash(self.path)
        return self._hash

    def __repr__(self):
        return f'<File({self._path})>'


class Folder():
    pass


class Syncronizer():
    pass
