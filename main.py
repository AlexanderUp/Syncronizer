# encoding:utf-8
# Syncronizer project
# main module

import os

from entities import File
from aux import get_hash


TEST_FILE = os.path.expanduser('~/Desktop/Python - my projects/syncronizer/test_files/dir_A/3DkOuDHh3mI.jpg')


if __name__ == '__main__':
    print('*' * 125)

    file = File(TEST_FILE)

    print(file)
    print(file.path)
    print(file.name)
    print(file.creation_time)
    print(file.access_time)
    print(file.modification_time)
    print(file.change_time)
    print(file.size)
    print('-' * 125)

    hash = get_hash(TEST_FILE)
    print(f'hash: {hash}')
    print(file.hash)
    print(file._hash)
    print('-' * 125)
