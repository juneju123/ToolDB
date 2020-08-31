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
from src.pre_and_post import global_vars

if __name__ == '__main__':
    helpers = global_vars.general_helpers
    helpers.log_config()
    my_logger = logging.getLogger(__name__)

    # Initial Variables
    result_files_list = []
    # Excluded some un-wanted symbols
    exclude_symbols = helpers.read_symbol_list('symbol_list/Exclude_Symbols.xlsx')
    # All optionable symbols
    symbol_list = helpers.read_symbol_list('symbol_list/Optionable.xlsx')
    # Filter symbols
    for symbol in exclude_symbols:
        if symbol in symbol_list:
            symbol_list.remove(symbol)
    # Get start time
    start_time = global_vars.ROUND_NAME
    is_live = False
    try:
        # Initiate Option tool instance
        handler = option_tool.OptionTool(global_vars.IS_GUI)
        # Run pre execution to get input parameters
        handler.pre_execution()
        # Execution
        result_files_list = handler.execution()
        # Prepare email messages and subject
        email_msg = "Test starts at: " + str(start_time) + "\nTest ends at: " + str(datetime.today().strftime(
            '%Y%m%d_%H%M')) + "\nResult folder: " + global_vars.RESULT_FOLDER + '\n' + "Raw data folder: " + \
                    global_vars.RAW_DATA_FOLDER + '\n'
        email_subject = global_vars.ROUND_NAME + "; is_live_data: " + str(is_live) + '; Option Screen Finished'
    except Exception as e:
        print(traceback.format_exc())
        my_logger.debug(traceback.format_exc())
        # Send exception information
        email_msg = "Exception happened on test: " + start_time
        email_subject = "Exception happened on test: " + start_time
        # send_notification(email_subject, traceback.format_exc(), [])
    finally:
        # Send email notification with results
        helpers.send_notification(email_subject, email_msg, result_files_list)
