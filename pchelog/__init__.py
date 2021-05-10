import configparser
import datetime
import os

import pymysql


class Logger:
    __name_time = ''
    __name = ''
    __str = ''
    __file = ''
    __file_time = ''
    __console_log = 'True'
    __file_log = 'none'
    __database_log = 'none'
    __service = 'example'
    __file_mode = 'default'

    def __init__(self, directory=''):
        if directory != '':
            self.__config = configparser.ConfigParser()
            self.__config.read(directory)
            self.__console_log = (self.__config['output']['console'])
            self.__file_log = (self.__config['output']['file'])
            self.__database_log = (self.__config['output']['mysql'])
            self.__service = self.__config['service']['name']
            self.__file_mode = self.__config['file']['mode']
            if self.__file_log != 'none':
                name_list = self.__config['file']['filename'].split('.')
                name_list.remove('txt')
                if self.__file_mode == 'current' or self.__file_mode == 'timestamp':
                    create_time = datetime.datetime.now()
                    self.__name_time = '.'.join(name_list) + '-'\
                        + str(datetime.date.today()) + '-'\
                        + str(create_time.hour) + '-'\
                        + str(create_time.minute) + '-'\
                        + str(create_time.second) + '.txt'
                    self.__file_time = os.path.join(self.__config['file']['directory'], self.__name_time)
                    self.__f_time = open(self.__file_time, 'w')
                if self.__file_mode == 'default' or self.__file_mode == 'timestamp':
                    self.__name = '.'.join(name_list) + '.txt'
                    self.__file = os.path.join(self.__config['file']['directory'], self.__name)
                    self.__f = open(self.__file, 'w')
            if self.__database_log != 'none':
                self.__conn = pymysql.connect(
                    host=self.__config['mysql']['host'],
                    port=int(self.__config['mysql']['port']),
                    user=self.__config['mysql']['user'],
                    password=self.__config['mysql']['password'],
                    database=self.__config['mysql']['database'],
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
        if self.__file_mode == 'default' or self.__file_mode == 'timestamp':
            self.__f.write(self.__str)
        if self.__file_mode == 'current' or self.__file_mode == 'timestamp':
            self.__f_time.write(self.__str)

    def __console_write(self, level, message, time):
        print(f'{time} | {message} | {self.__service} | {level}')

    def debug(self, message):
        time = datetime.datetime.now()
        if self.__console_log != 'none':
            self.__console_write('DEBUG', message, time)
        if self.__database_log != 'none':
            self.__db_write('DEBUG', message, time)
        if self.__file_log != 'none':
            self.__file_write('DEBUG', message, time)

    def info(self, message):
        time = datetime.datetime.now()
        if self.__console_log != 'none':
            self.__console_write('INFO', message, time)
        if self.__database_log != 'none':
            self.__db_write('INFO', message, time)
        if self.__file_log != 'none':
            self.__file_write('INFO', message, time)

    def warning(self, message):
        time = datetime.datetime.now()
        if self.__console_log != 'none':
            self.__console_write('WARNING', message, time)
        if self.__database_log != 'none':
            self.__db_write('WARNING', message, time)
        if self.__file_log != 'none':
            self.__file_write('WARNING', message, time)

    def error(self, message):
        time = datetime.datetime.now()
        if self.__console_log != 'none':
            self.__console_write('ERROR', message, time)
        if self.__database_log != 'none':
            self.__db_write('ERROR', message, time)
        if self.__file_log != 'none':
            self.__file_write('ERROR', message, time)

    def critical(self, message):
        time = datetime.datetime.now()
        if self.__console_log != 'none':
            self.__console_write('CRITICAL', message, time)
        if self.__database_log != 'none':
            self.__db_write('CRITICAL', message, time)
        if self.__file_log != 'none':
            self.__file_write('CRITICAL', message, time)
