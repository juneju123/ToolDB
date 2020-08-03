#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      2:13 PM
@Author:    Juju
@File:      FileHelpers
@Project:   OptionToolDb
"""
import logging.config
import os

from pandas import read_excel

from src.pre_and_post import global_vars


class FileHelpers:
    def __init__(self):
        pass

    @staticmethod
    def read_string_from_file(file_path):
        with open(file_path, 'r') as file:
            return file.readline()

    @staticmethod
    def read_symbol_list(file_path):
        return read_excel(file_path, sheet_name=0)['symbol'].tolist()

    @staticmethod
    def save_spread_to_csv(spread, spread_type, conditions):
        if not os.path.exists(global_vars.RESULT_FOLDER):
            os.makedirs(global_vars.RESULT_FOLDER)
        output_file = global_vars.RESULT_FOLDER + spread_type + '_' + '_'.join(conditions) + '.csv'
        spread.to_csv(output_file)
        return output_file

    @staticmethod
    def log_config():
        """
        Config log with dict
        Returns: None

        """
        log_config_dict = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': '%(asctime)-15s, %(levelname)s, %(name)s, Line: %(lineno)d, Process: %(process)d, Message: %(message)s',
                    'datefmt': '%a %d %b %Y %H:%M:%S'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'simple',
                    'stream': 'ext://sys.stdout'
                },
                'info_file_handler': {
                    'class': 'logging.FileHandler',
                    'level': 'INFO',
                    'formatter': 'simple',
                    'filename': 'debug.log',
                    'encoding': 'utf8',
                    'mode': 'w'
                }
            },
            'loggers': {
                '': {
                    'level': 'INFO',
                    'handlers': ['console', 'info_file_handler'],
                    'propagate': False
                }
            }
        }
        logging.config.dictConfig(log_config_dict)
        return None
