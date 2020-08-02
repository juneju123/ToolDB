#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      2:13 PM
@Author:    Juju
@File:      FileHelpers
@Project:   OptionToolDb
"""
import os

from pandas import read_excel

import global_vars


def read_string_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.readline()


def read_symbol_list(file_path):
    return read_excel(file_path, sheet_name=0)['symbol'].tolist()


def save_spread_to_csv(spread, spread_type, conditions):
    if not os.path.exists(global_vars.RESULT_FOLDER):
        os.makedirs(global_vars.RESULT_FOLDER)
    output_file = global_vars.RESULT_FOLDER + spread_type + '_' + '_'.join(conditions) + '.csv'
    spread.to_csv(output_file)
    return output_file
