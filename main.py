# encoding:utf-8
# Syncronizer project
# main module

import os

from class_file import File
from class_folder import Folder
from syncronizer import Syncronizer
from app_logger import get_logger


TEST_FILE_A = os.path.expanduser('~/Desktop/Python - my projects/syncronizer/test_files/dir_A/3DkOuDHh3mI.jpg')
TEST_FILE_B = os.path.expanduser('~/Desktop/Python - my projects/syncronizer/test_files/dir_B/B-c-eEAzwbQ.jpg')
TEST_FILE_C = os.path.expanduser('~/Desktop/Python - my projects/syncronizer/test_files/dir_B/dir_B_sub_B/dir_B_sub_B_sub_C/lossless.png')
TEST_FOLDER_A = os.path.expanduser('~/Desktop/Python - my projects/syncronizer/test_files/dir_A')
TEST_FOLDER_B = os.path.expanduser('~/Desktop/Python - my projects/syncronizer/test_files/dir_B')
TEST_FOLDER_C = os.path.expanduser('~/Desktop/Python - my projects/syncronizer/test_files/dir_C')
TEST_FOLDER_D = os.path.expanduser('~/Desktop/Python - my projects/syncronizer/test_files/dir_D')


if __name__ == '__main__':
    print('*' * 125)

    logger = get_logger(__name__)
    logger.info('Logger started')

    # folder_A = Folder(TEST_FOLDER_A)
    # folder_B = Folder(TEST_FOLDER_B)
    folder_C = Folder(TEST_FOLDER_C)
    folder_D = Folder(TEST_FOLDER_D)
    # logger.debug(f'Folder A: {folder_A}')
    # logger.debug(f'Folder B: {folder_B}')
    logger.debug(f'Folder C: {folder_C}')
    logger.debug(f'Folder D: {folder_D}')
    print('-' * 125)

    # logger.debug(f'len folder A: {len(folder_A)}')
    # logger.debug(f'len folder B: {len(folder_B)}')
    logger.debug(f'len folder C: {len(folder_C)}')
    logger.debug(f'len folder D: {len(folder_D)}')
    print('-' * 125)

    syncro = Syncronizer()
    syncro.add_left_side(folder_C)
    syncro.add_right_side(folder_D)
    print(syncro)
    print('-' * 125)

    # print('Relative path from TEST_FILE_C to TEST_FOLDER_B:')
    # print(f'... by Syncronizer: {syncro._get_file_relative_path(TEST_FILE_C, folder_B)}')
    # print(f'... by <os.path.relpath>: {os.path.relpath(TEST_FILE_C, start=TEST_FOLDER_B)}')
    # print('-' * 125)

    # syncro.update_db_with_hashes()
    # print('-' * 125)

    syncro.report()
    print('-' * 125)

    for file in syncro._files_from_left_to_right:
        print(file)
    print('-' * 125)

    for file in syncro._files_from_right_to_left:
        print(file)
    print('-' * 125)

    # syncro.syncronize()
    # print('-' * 125)

    # session = folder_C._create_session()
    # print('-' * 125)

    # syncro._get_deleted_files(folder_D)
    # print('-' * 125)
