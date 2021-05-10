import configparser
import datetime
import os

import pymysql


class DatabaseFileLogger:
    __str = ''
    __file = ''
    __console_log = True
    __file_log = False
    __database_log = False
    __service = 'example'

    def __init__(self, directory):
        if directory != '':
            self.__config = configparser.ConfigParser()
            self.__config.read(directory)
            self.__console_log = bool(self.__config['console']['bool'])
            self.__file_log = bool(self.__config['file']['bool'])
            self.__database_log = bool(self.__config['database']['bool'])
            self.__service = self.__config['service']['name']
            if self.__file_log:
                self.__file = os.path.join(self.__config['file']['directory'], self.__config['file']['filename'])
                self.__f = open(self.__file, 'a')
            if self.__database_log:
                self.__conn = pymysql.connect(
                    host=self.__config['database']['host'],
                    port=int(self.__config['database']['port']),
                    user=self.__config['database']['user'],
                    password=self.__config['database']['password'],
                    database=self.__config['database']['database'],
                    cursorclass=pymysql.cursors.DictCursor
                )
                self.__cursor = self.__conn.cursor()

    def __db_write(self, level, message, time):
        logg = [(time, message, self.__service, level)]
        self.__cursor.executemany(
            'INSERT INTO logs (datetime, message, service, level) VALUES (%s,%s,%s,%s)', logg)
        self.__conn.commit()

    def __file_write(self, level, message, time):
        self.__str = str(time) + ' | ' + message + ' | ' + self.__service + ' | ' + level + '\n'
        self.__f.write(self.__str)

    def __console_write(self, level, message, time):
        print(f'{time} | {message} | {self.__service} | {level}')

    def debug(self, message):
        time = datetime.datetime.now()
        if self.__console_log:
            self.__console_write('DEBUG', message, time)
        if self.__database_log:
            self.__db_write('DEBUG', message, time)
        if self.__file_log:
            self.__file_write('DEBUG', message, time)

    def info(self, message):
        time = datetime.datetime.now()
        if self.__console_log:
            self.__console_write('INFO', message, time)
        if self.__database_log:
            self.__db_write('INFO', message, time)
        if self.__file_log:
            self.__file_write('INFO', message, time)

    def warning(self, message):
        time = datetime.datetime.now()
        if self.__console_log:
            self.__console_write('WARNING', message, time)
        if self.__database_log:
            self.__db_write('WARNING', message, time)
        if self.__file_log:
            self.__file_write('WARNING', message, time)

    def error(self, message):
        time = datetime.datetime.now()
        if self.__console_log:
            self.__console_write('ERROR', message, time)
        if self.__database_log:
            self.__db_write('ERROR', message, time)
        if self.__file_log:
            self.__file_write('ERROR', message, time)

    def critical(self, message):
        time = datetime.datetime.now()
        if self.__console_log:
            self.__console_write('CRITICAL', message, time)
        if self.__database_log:
            self.__db_write('CRITICAL', message, time)
        if self.__file_log:
            self.__file_write('CRITICAL', message, time)
