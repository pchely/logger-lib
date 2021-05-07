import datetime
import pymysql
import configparser


class DatabaseLog:
    __str = ''
    __file = ''
    __service = ''

    def __init__(self, directory):
        self.__config = configparser.ConfigParser()
        self.__config.read(directory)
        self.__service = self.__config['service']['name']
        self.__file = self.__config['file']['directory'] + '\\' + self.__config['file']['filename']
        self.__conn = pymysql.connect(
            host=self.__config['database']['host'],
            port=int(self.__config['database']['port']),
            user=self.__config['database']['user'],
            password=self.__config['database']['password'],
            database=self.__config['database']['database'],
            cursorclass=pymysql.cursors.DictCursor
        )
        self.__cursor = self.__conn.cursor()
        self.__f = open(self.__file, 'a')

    def __db_write(self, level, message, time):
        logg = [(time, message, self.__service, level)]
        self.__cursor.executemany(
            "INSERT INTO logs (datetime, message,  service, level) VALUES (%s,%s,%s,%s)", logg)
        self.__conn.commit()

    def __file_write(self, level, message, time):
        self.__str = str(time) + ' | ' + message + ' | ' + self.__service + ' | ' + level + '\n'
        self.__f.write(self.__str)

    def debug(self, message):
        time = datetime.datetime.now()
        self.__db_write('DEBUG', message, time)
        self.__file_write('DEBUG', message, time)

    def info(self, message):
        time = datetime.datetime.now()
        self.__db_write('INFO', message, time)
        self.__file_write('INFO', message, time)

    def warning(self, message):
        time = datetime.datetime.now()
        self.__db_write('WARNING', message, time)
        self.__file_write('WARNING', message, time)

    def error(self, message):
        time = datetime.datetime.now()
        self.__db_write('ERROR', message, time)
        self.__file_write('ERROR', message, time)

    def critical(self, message):
        time = datetime.datetime.now()
        self.__db_write('CRITICAL', message, time)
        self.__file_write('CRITICAL', message, time)
