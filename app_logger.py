# encoding:utf-8
# Syncronizer project
# logging instance


import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    logger.addHandler(consoleHandler)
    formatter = logging.Formatter('[%(name)s] [%(levelname)s] <%(module)s> %(message)s')
    consoleHandler.setFormatter(formatter)
    return logger
