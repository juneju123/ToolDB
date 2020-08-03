#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      2:11 PM
@Author:    Juju
@File:      Main
@Project:   OptionToolDb
"""
import logging
import traceback
from datetime import datetime

from src.core import option_tool
from src.helpers import file_helpers, log_config
from src.pre_and_post import global_vars
from src.pre_and_post.send_notification import send_notification

if __name__ == '__main__':
    log_config.log_config()
    my_logger = logging.getLogger(__name__)

    # Initial Variables
    result_files_list = []
    exclude_symbols = file_helpers.read_symbol_list('symbol_list/Exclude_Symbols.xlsx')
    symbol_list = file_helpers.read_symbol_list('symbol_list/Optionable.xlsx')
    # symbol_list = ['SPY']
    for symbol in exclude_symbols:
        if symbol in symbol_list:
            symbol_list.remove(symbol)

    start_time = global_vars.ROUND_NAME
    is_live = False
    try:
        handler = option_tool.OptionTool()
        handler.pre_execution()

        result_files_list = handler.execution()
        email_msg = "Test starts at: " + str(start_time) + "\nTest ends at: " + str(datetime.today().strftime(
            '%Y%m%d_%H%M')) + "\nResult folder: " + global_vars.RESULT_FOLDER + '\n' + "Raw data folder: " + \
                    global_vars.RAW_DATA_FOLDER + '\n'
        email_subject = global_vars.ROUND_NAME + "; is_live_data: " + str(is_live) + '; Option Screen Finished'

    except Exception as e:
        print(traceback.format_exc())
        my_logger.debug(traceback.format_exc())
        # Send exception information
        # email_msg = "Exception happened on test: " + start_time
        # email_subject = "Exception happened on test: " + start_time
        # send_notification(email_subject, traceback.format_exc(), [])
    finally:
        # Send email notification with results
        send_notification(email_subject, email_msg, result_files_list)

