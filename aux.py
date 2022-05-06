# encoding:utf-8
# Syncronizer project
# auxiliary functions

from hashlib import sha256

FILE_CHUNK = 1024 * 1024 # one megabyte


def get_hash(file):
    with open(file, 'rb') as source:
        hasher = sha256()
        while chunk := source.read(FILE_CHUNK):
            hasher.update(chunk)
    return hasher.hexdigest()
