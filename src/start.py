#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      2:11 PM
@Author:    Juju
@File:      Main
@Project:   OptionToolDb
"""
import traceback
from datetime import datetime

from src.core import option_tool
from src.pre_and_post import global_vars


def start(log_handler):
    helpers = global_vars.general_helpers
    my_logger = log_handler
    my_logger.info("Hello!!!")

    # Initial Variables
    result_files_list = []
    start_time = global_vars.ROUND_NAME
    is_live = False
    try:
        # Initiate Option tool instance
        handler = option_tool.OptionTool(global_vars.IS_GUI, my_logger)
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
        # helpers.send_notification(email_subject, email_msg, result_files_list)
        global_vars.RESULT_LIST = result_files_list
