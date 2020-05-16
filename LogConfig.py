#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Custom logging configuration."""
"""
# @Time    : 9/22/2017 6:42 PM
# @Author  : Juju
# @File    : LogConfig.py
"""

import logging.config


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
