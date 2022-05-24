# encoding:utf-8
# Syncronizer project
# main module

from pathlib import Path

from class_file import File
from class_folder import Folder
from syncronizer import Syncronizer
from app_logger import get_logger


TEST_FILE_A = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_A/3DkOuDHh3mI.jpg').expanduser()
TEST_FILE_B = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_B/B-c-eEAzwbQ.jpg').expanduser()
TEST_FILE_C = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_B/dir_B_sub_B/dir_B_sub_B_sub_C/lossless.png').expanduser()
TEST_FOLDER_A = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_A').expanduser()
TEST_FOLDER_B = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_B').expanduser()
TEST_FOLDER_C = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_C').expanduser()
TEST_FOLDER_D = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_D').expanduser()


if __name__ == '__main__':
    print('*' * 125)

    logger = get_logger(__name__)
    logger.info('Logger started')

    logger.debug(f'Folder A (path): {TEST_FOLDER_A}')
    logger.debug(f'Folder B (path): {TEST_FOLDER_B}')

    folder_A = Folder(TEST_FOLDER_A)
    folder_B = Folder(TEST_FOLDER_B)
    folder_C = Folder(TEST_FOLDER_C)
    folder_D = Folder(TEST_FOLDER_D)
    logger.debug(f'Folder A: {folder_A}')
    logger.debug(f'Folder B: {folder_B}')
    logger.debug(f'Folder C: {folder_C}')
    logger.debug(f'Folder D: {folder_D}')
    print('-' * 125)

    logger.debug(f'len folder A: {len(folder_A)}')
    logger.debug(f'len folder B: {len(folder_B)}')
    logger.debug(f'len folder C: {len(folder_C)}')
    logger.debug(f'len folder D: {len(folder_D)}')
    print('-' * 125)

    syncro = Syncronizer()
    syncro.add_left_side(folder_C)
    syncro.add_right_side(folder_D)
    print(syncro)
    print('-' * 125)

    syncro.report()
    print('-' * 125)

    # syncro.syncronize()
    # print('-' * 125)

    # session = folder_C._create_session()
    print('-' * 125)
