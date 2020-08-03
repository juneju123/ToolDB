#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      3:43 PM
@Author:    Juju
@File:      OptionDb
@Project:   OptionToolDb
"""
import pymysql

from src.helpers.file_helpers import read_string_from_file


class OptionDbHelpers:
    def __init__(self, db_name):
        db_key = read_string_from_file("src/private_info/db_key")
        self.conn = pymysql.connect('localhost', 'root', db_key, db_name)

    def create_option_table(self, table_name, columns):
        with self.conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS " + table_name)
            sql = "CREATE TABLE %s ( %s ) " % (table_name, columns)
            cursor.execute(sql)

    def insert_dict(self, table_name, dt):
        with self.conn.cursor() as cursor:
            placeholders = ', '.join(['%s'] * len(dt))
            columns = ', '.join(dt.keys())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, columns, placeholders)
            try:
                cursor.execute(sql, list(dt.values()))
            except TypeError:
                pass

    def read_rows(self, table_name, **kwargs):
        conditions = kwargs.get("conditions", None)
        with self.conn.cursor() as cursor:
            if conditions is None:
                cursor.execute("SELECT * FROM " + table_name)
            else:
                cursor.execute("SELECT * FROM " + table_name + " WHERE " + conditions)
            result = cursor.fetchall()
        return result

    def get_columns_names(self, table_name):
        column_names = []
        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % table_name
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        for column_name in result:
            column_names.append(column_name[0])
        return column_names

    def conn_commit(self):
        self.conn.commit()

    def conn_close(self):
        self.conn.close()
