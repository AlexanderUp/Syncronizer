# encoding:utf-8
# Syncronizer project
# auxiliary functions

import os

import config

from hashlib import sha256

from app_logger import get_logger


FILE_CHUNK = 1024 * 1024 # one megabyte


logger = get_logger(__name__)
conf = config.Config()


def get_hash(file, algo=sha256):
    with open(file, 'rb') as source:
        hasher = algo()
        while chunk := source.read(FILE_CHUNK):
            hasher.update(chunk)
    return (hasher.name, hasher.hexdigest())

def register_file_name_check_func(func):
    logger.info(f'Registred: {func.__name__}')
    conf.FILE_NAME_CHECK_FUNCS.append(func)
    return None

@register_file_name_check_func
def is_hidden_file(path_to_file):
    file_name = os.path.basename(path_to_file)
    return file_name.startswith('.')

@register_file_name_check_func
def is_db_file(path_to_file):
    head, tail = os.path.split(path_to_file)
    return tail == f'_{os.path.basename(head)}_{conf.DB_NAME_TEMPLATE}'

#############################################################################

# TODO: move to aux.py
def _create_session(self, folder):
    path_to_db = os.path.join(folder.path, f'_{os.path.basename(folder.path)}_{conf.DB_NAME_TEMPLATE}')
    engine = create_engine('sqlite:///' + path_to_db)
    logger.info(f'DB engine: {engine}')
    metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    logger.debug(f'Session: {session}')
    return session

# ???
def _add_to_db(self, file_obj):
    self.session.add(file_obj)
    try:
        self.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as err:
        logger.error(f'{err}')
        self.session.rollback()
    else:
        logger.debug(f'Successfully commited: {file_obj}')
    return None

# TODO: move to aux.py
def _update_db_with_hashes(self, session):
    queried_files = session.query(File).all()
    for file in queried_files:
        if not os.path.exists(file.path):
            logger.debug(f'Not exists: {file}')
            continue
        file.calculate_hash()
        session.add(file)
        try:
            session.commit()
        except sqlalchemy.exc.SQLAlchemyError as err:
            logger.error(f'{err}')
            session.rollback()
        else:
            logger.debug(f'Successfully commited: {file}')
    return None

def _get_deleted_files(self, session):
    deleted_files = []
    queried_files = session.query(File).all()

    for file in queried_files:
        if not os.path.exists(file.path):
            logger.debug(f'Deleted: {file}')
            deleted_files.append(file)
    return deleted_files

def _get_deleted_files(self, folder):
    session = self._create_session(folder)
    retrived_file_entries = session.query(File).all()
    if not retrived_file_entries:
        print('No deleted files!')
    for file in retrived_file_entries:
        print(file)
    return None

def _save_state(self):
    pass

def _load_state(self):
    pass

def cleanup_db(self, session):
    pass
