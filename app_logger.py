# encoding:utf-8
# Syncronizer project
# logging instance


import logging
import datetime


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    logger.addHandler(consoleHandler)
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] N: [%(name)s] M: <%(module)s> F: <%(funcName)s> | %(message)s',
                                    datefmt=logging.Formatter.default_time_format)
    consoleHandler.setFormatter(formatter)
    return logger
