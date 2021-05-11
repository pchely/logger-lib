import configparser
import datetime
import json
import os
import requests

import pymysql


class Logger:
    __level = {
        'none': -1,
        'debug': 50,
        'info': 40,
        'warning': 30,
        'error': 20,
        'critical': 10
    }
    __name_time = ''
    __name = ''
    __str = ''
    __file = ''
    __file_time = ''
    __console_log = 50
    __file_log = -1
    __database_log = -1
    __slack_log = -1
    __service = 'example'
    __file_mode = 'default'

    def __init__(self, directory=''):
        if directory != '':
            self.__config = configparser.ConfigParser()
            self.__config.read(directory)
            self.__console_log = self.__level[str(self.__config['output']['console'])]
            self.__file_log = self.__level[str(self.__config['output']['file'])]
            self.__database_log = self.__level[str(self.__config['output']['mysql'])]
            self.__slack_log = self.__level[str(self.__config['output']['slack'])]
            self.__service = self.__config['service']['name']
            if self.__file_log != -1:
                self.__file_mode = self.__config['file']['mode']
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
            if self.__database_log != -1:
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

    def __slack_web_hook_write(self, level, message, time):
        self.__str = str(time) + ' | ' + message + ' | ' + self.__service + ' | ' + level
        slack_msg = {'message': self.__str}
        requests.post(self.__config['slack']['web_hook_url'], data=json.dumps(slack_msg))

    def debug(self, message):
        time = datetime.datetime.now()
        if self.__console_log > 40:
            self.__console_write('DEBUG', message, time)
        if self.__database_log > 40:
            self.__db_write('DEBUG', message, time)
        if self.__file_log > 40:
            self.__file_write('DEBUG', message, time)
        if self.__slack_log > 40:
            self.__slack_web_hook_write('DEBUG', message, time)

    def info(self, message):
        time = datetime.datetime.now()
        if self.__console_log > 30:
            self.__console_write('INFO', message, time)
        if self.__database_log > 30:
            self.__db_write('INFO', message, time)
        if self.__file_log > 30:
            self.__file_write('INFO', message, time)
        if self.__slack_log > 30:
            self.__slack_web_hook_write('INFO', message, time)

    def warning(self, message):
        time = datetime.datetime.now()
        if self.__console_log > 20:
            self.__console_write('WARNING', message, time)
        if self.__database_log > 20:
            self.__db_write('WARNING', message, time)
        if self.__file_log > 20:
            self.__file_write('WARNING', message, time)
        if self.__slack_log > 20:
            self.__slack_web_hook_write('WARNING', message, time)

    def error(self, message):
        time = datetime.datetime.now()
        if self.__console_log > 10:
            self.__console_write('ERROR', message, time)
        if self.__database_log > 10:
            self.__db_write('ERROR', message, time)
        if self.__file_log > 10:
            self.__file_write('ERROR', message, time)
        if self.__slack_log > 10:
            self.__slack_web_hook_write('ERROR', message, time)

    def critical(self, message):
        time = datetime.datetime.now()
        if self.__console_log > 0:
            self.__console_write('CRITICAL', message, time)
        if self.__database_log > 0:
            self.__db_write('CRITICAL', message, time)
        if self.__file_log > 0:
            self.__file_write('CRITICAL', message, time)
        if self.__slack_log > 0:
            self.__slack_web_hook_write('CRITICAL', message, time)
