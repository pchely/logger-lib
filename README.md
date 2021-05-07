# logger-lib
Библиотека с возможностью логирования в MySQL БД и в файл
### Запуск
-Скачать файл logs_class в свой проект

-установить библиотеку pymysql
```
pip install pymysql
```
-подключить класс из файла
```Python
from logs_class import DatabaseLog
```

### Работа с классом
-создание экземпляра
```Python
log = DatabaseLog('loggers.ini')
```
settings.ini заполняется из примера loggers.example.ini

Методы класса обозначают уровень лога от `INFO` до `CRITICAL`

В параметр стоит написать описание ошибки:
```Python
log.warning('your message')
```

### Принцип работы
При создание экземпляра передается файл loggers.ini

[database] - данные, необходимые для подключение к БД

[file]:
  - [directory] - директория, где лежит файл для записи логов
  - [filename] - имя файла, куда будут записаны логи

[service] - название сервиса/проекта, в котором Вы работаете

При вызове метода сообщение, время, уровень ошибки и название сервиса записывается в БД и файл в формате:
```
time | message | service | level
```

Таблица из БД:

```SQL
create table table_name
(
    id       int auto_increment
        primary key,
    datetime datetime default CURRENT_TIMESTAMP not null,
    message  varchar(255)                       not null,
    service  varchar(255)                       not null,
    level    varchar(255)                       not null
);
```
