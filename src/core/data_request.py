#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      4:24 PM
@Author:    Juju
@File:      InitialData
@Project:   OptionToolDb
"""
import logging

import pymysql
from tqdm import tqdm

from src.helpers import process_helpers
from src.option_objects import option_chain, DateChain, single_option_obj
from src.process import tda_api_request


class DataRequest:
    def __init__(self, symbol_list, db_conn, real_data):
        self.symbol_list = symbol_list
        self.db_conn = db_conn
        self.real_data = real_data

    def request_all_data(self):
        my_logger = logging.getLogger(__name__)
        option_column_names = """underlying_symbol CHAR(10), underlying_price FLOAT, putCall CHAR(5), 
            symbol CHAR(20), description VARCHAR(50), exchangeName CHAR(10), bid FLOAT, ask FLOAT, last FLOAT, mark FLOAT, 
            bidSize INT, askSize INT, bidAskSize CHAR(20), lastSize INT, highPrice FLOAT, lowPrice FLOAT, openPrice FLOAT, 
            closePrice FLOAT, totalVolume INT, tradeTimeInLong DATE, quoteTimeInLong DATE, netChange FLOAT, 
            volatility FLOAT, delta FLOAT, gamma FLOAT, theta FLOAT, vega FLOAT, rho FLOAT, openInterest INT, 
            timeValue FLOAT, theoreticalOptionValue FLOAT, theoreticalVolatility FLOAT, strikePrice FLOAT, 
            expirationDate DATE, daysToExpiration INT, expirationType CHAR(5), lastTradingDay DATE, multiplier FLOAT, 
            percentChange FLOAT, markChange FLOAT, 
            markPercentChange FLOAT, nonStandard CHAR(5), inTheMoney CHAR(5), mini CHAR(5), bidAskSpread FLOAT, 
            probITM FLOAT"""

        if self.real_data:
            my_logger.info('Request real data.....')
            for symbol in tqdm(self.symbol_list):
                self.db_conn.create_option_table(symbol + '_options', option_column_names)
                try:
                    response = tda_api_request.request_option_chain(symbol=symbol)
                except tda_api_request.RequestError:
                    continue
                underlying_price = response['underlyingPrice']
                underlying_symbol = response['symbol']
                call_date_map = response['callExpDateMap']
                put_date_map = response['putExpDateMap']
                for date_map in [call_date_map, put_date_map]:
                    for date_string in date_map.keys():
                        date_chain = date_map[date_string]
                        for strike in date_chain.keys():
                            option = date_chain[strike][0]
                            if option['totalVolume'] == 0 or option['theoreticalOptionValue'] == -999:
                                continue
                            option = process_helpers.clean_option_dict(option, underlying_price, underlying_symbol)
                            try:
                                self.db_conn.insert_dict(symbol + '_options', option)
                            except pymysql.err.DataError:
                                pass
            self.db_conn.conn_commit()
            my_logger.info('All data stored to Database')
        my_logger.info('Fetch all call options from Database...')
        all_call_chains = self.get_all_chains('CALL')
        print('\n')
        my_logger.info('Fetch all put options from Database...')
        all_put_chains = self.get_all_chains('PUT')
        return all_call_chains, all_put_chains

    def get_all_chains(self, put_call):
        all_options = {}
        for symbol in tqdm(self.symbol_list):
            if put_call == 'PUT':
                options = self.db_conn.read_rows(symbol + '_options', conditions='putCALL = \'PUT\'')
            else:
                options = self.db_conn.read_rows(symbol + '_options', conditions='putCALL = \'CALL\'')
            all_options[symbol] = options

        all_symbols_chains = {}
        for symbol in self.symbol_list:
            all_symbols_chains[symbol] = option_chain.OptionChain(symbol)
            for n in range(len(all_options[symbol])):
                single_option = single_option_obj.SingleOption(all_options[symbol][n])
                expiration = single_option.get_expiration_date()
                strike = single_option.get_strike()
                if not all_symbols_chains[symbol].has_date_chain(expiration):
                    date_chain = DateChain.DateChain()
                    date_chain.append_single_option(strike, single_option)
                    all_symbols_chains[symbol].append_date_chain(expiration, date_chain)
                else:
                    date_chain = all_symbols_chains[symbol].get_date_chain(expiration)
                    date_chain.append_single_option(strike, single_option)

        return all_symbols_chains
