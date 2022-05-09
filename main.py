# encoding:utf-8
# Syncronizer project
# main module

from pathlib import Path

from entities import File
from entities import Folder
from app_logger import get_logger


TEST_FILE_A = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_A/3DkOuDHh3mI.jpg').expanduser()
TEST_FILE_B = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_B/B-c-eEAzwbQ.jpg').expanduser()
TEST_FILE_C = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_B/dir_B_sub_B/dir_B_sub_B_sub_C/lossless.png').expanduser()
TEST_FOLDER_A = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_A').expanduser()
TEST_FOLDER_B = Path('~/Desktop/Python - my projects/syncronizer/test_files/dir_B').expanduser()


if __name__ == '__main__':
    print('*' * 125)
    logger = get_logger(__name__)
    logger.info('Logger started')

    logger.debug(f'Folder A (path): {TEST_FOLDER_A}')
    logger.debug(f'Folder B (path): {TEST_FOLDER_B}')

    folder_A = Folder(TEST_FOLDER_A)
    folder_B = Folder(TEST_FOLDER_B)
    logger.debug(f'Folder A: {folder_A}')
    logger.debug(f'Folder B: {folder_B}')
    print('-' * 125)

    logger.debug(f'len folder A: {len(folder_A)}')
    logger.debug(f'len folder B: {len(folder_B)}')

    logger.debug('Difference (A to B):')
    difference_A_B = folder_A.difference(folder_B)
    for file in difference_A_B:
        logger.debug(file)
    print('-' * 125)

    logger.debug('Difference (B to A):')
    difference_B_A = folder_B.difference(folder_A)
    for file in difference_B_A:
        logger.debug(file)
    print('-' * 125)
