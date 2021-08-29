# pchelog

Библиотека с возможностью логирования в MySQL, PostgreSQL, файл и Slack Workflow Webhook.

Пакет находится в разработке, не рекомендуется к использованию в production.

## Установка и использование

Перед тем, как использовать библиотеку логгера необходимо создать таблицу в вашей MySQL БД:

```mysql
create table table_name
(
    id       int auto_increment primary key,
    timestamp datetime default CURRENT_TIMESTAMP not null,
    message  varchar(255)                       not null,
    service  varchar(255)                       not null,
    level    varchar(255)                       not null
);
```

Установить библиотеку можно с помощью pip:

```shell
pip install git+https://github.com/pchely/pchelog.git
```

Создайте в корне своего проекта файл logger.ini и заполните его:

```ini
; название вашего сервиса
[service]
name = my-awesome-project

; минимальный уровень, с которого логировать в этот вывод: 
; none, debug, info, warning, error, critical
[output]
console = debug
mysql = warning
postgres = info
file = info
slack = error

; СУБД
[typedatabase]
type = mysql, postgres, mysql_postgres(логи записываются в обе БД)

; раздел не обязателен, если вывод в Slack отключен
[slack]
url = https://hooks.slack.com/workflows/123/12/123/123456

; раздел не обязателен, если вывод в MySQL отключен
[mysql]
host = localhost
port = 3306
user = ivanlut
password = passwd
database = logs
table = logs

; раздел не обязателен, если вывод в PostgreSQL отключен
[postgres]
host = localhost
port = 5432
user = postgres
password = passwd
database = logs
table = logs

; раздел не обязателен, если вывод в файл отключен
[file]
; пустой параметр означает, что файл с логами будет сохранен в корне проекта
directory =
; название файла (указывать формат файла не обязательно)
filename = log.txt
; доступные режимы работы с файлами:
; default - сохранение логов текущего запуска программы и предыдущих запусков в одном файле <filename>.txt
; current - сохранение только логов текущего запуска программы в файл <filename>.txt, предыдущие будут удаляться
; timestamp - запись логов текущего запуска в <filename>.txt и <filename>-<timestamp>.txt
mode = default

```

Импортируйте класс логгера из библиотеки:

```python
from pchelog import Logger

log = Logger('logger.ini')
```

И логируйте!

```python
log.debug('your message')
log.info('your message')
log.warning('your message')
log.error('your message')
log.critical('your message')
```

## Roadmap

- [x] установка через pip
- [x] вывод логов в консоль
- [x] выбор куда логировать: консоль/БД/файл
- [x] вывод в Slack Workflow Webhook
- [x] логи в отдельном файле с timestamp `log-timestamp.txt`
