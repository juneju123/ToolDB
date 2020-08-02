#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      2:14 PM
@Author:    Juju
@File:      TDA_API_Request
@Project:   OptionToolDb
"""


import logging
import time
from datetime import datetime, timedelta

import pandas as pd
import requests

from file_helpers import read_string_from_file

API_KEY = read_string_from_file('API_KEY')
my_logger = logging.getLogger(__name__)


def request_option_chain(**kwargs):
    """
    Request option chain via TD-Ameritrade API
    :param kwargs:
        symbol: symbol of underlying stock/etf
        strikeCount: number of strikes want to request
        includeQuotes: Include quotes for options in the option chain. Can be TRUE or FALSE. Default is FALSE.
        strategy: Passing a value returns a Strategy Chain. Possible values are SINGLE, ANALYTICAL (allows use of the
                volatility, underlyingPrice, interestRate, and daysToExpiration params to calculate theoretical values),
                COVERED, VERTICAL, CALENDAR, STRANGLE, STRADDLE, BUTTERFLY, CONDOR, DIAGONAL, COLLAR, or ROLL. Default
                is SINGLE.
        minDaysToExpiration: minimal days to expiration
        maxDaysToExpiration: maximal days to expiration
    :return: Option chain in JSON format
    """
    url = "https://api.tdameritrade.com/v1/marketdata/chains?{}".format(kwargs.get('symbol'))

    params = {}
    params.update({'apikey': API_KEY})
    params.update({'range': 'ALL'})
    now = datetime.now()

    for arg in kwargs:
        if arg == 'minDaysToExpiration':
            from_date = (now + timedelta(days=kwargs.get(arg))).date()
            parameter = {'fromDate': from_date}
        elif arg == 'maxDaysToExpiration':
            to_date = (now + timedelta(days=kwargs.get(arg))).date()
            parameter = {'toDate': to_date}
        else:
            parameter = {arg: kwargs.get(arg)}
        params.update(parameter)
    return robust_request(url, params)


def request_price_history(**kwargs):
    url = "https://api.tdameritrade.com/v1/marketdata/{}/pricehistory?".format(kwargs.get('symbol'))
    params = {}
    params.update({'apikey': API_KEY})
    for arg in kwargs:
        parameter = {arg: kwargs.get(arg)}
        params.update(parameter)
    response = robust_request(url, params)
    response = response['candles']
    response_df = pd.DataFrame(response)
    response_df['datetime'] = pd.to_datetime(response_df['datetime'], unit='ms')
    response_df['datetime'] = response_df['datetime'].dt.strftime('%Y-%m-%d')
    response_df = response_df.set_index('datetime')
    return response_df


def request_fundamental(**kwargs):
    url = "https://api.tdameritrade.com/v1/instruments/?"
    params = {}
    params.update({'apikey': API_KEY})
    params.update({'symbol': kwargs.get('symbol')})
    params.update({'projection': 'fundamental'})
    response = robust_request(url, params)
    return response[kwargs.get('symbol')]['fundamental']


def robust_request(url, params):
    retry = 0
    fail_request = True
    while retry <= 2 and fail_request:
        response = requests.get(url, params=params)
        if response is None:
            my_logger.error("Retry " + params['symbol'])
            retry += 1
            time.sleep(3)
        elif response.status_code != 200:
            my_logger.error("Retry " + params['symbol'])
            retry += 1
            time.sleep(3)
        else:
            fail_request = False
    if fail_request:
        my_logger.error(response.request.url)
        raise RequestError(params['symbol'])
    return response.json()


class RequestError(Exception):
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        print("Request failed on " + self.symbol)


