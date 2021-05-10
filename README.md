# pchelog

Библиотека с возможностью логирования в MySQL БД, файл и Slack Workflow Webhook.

Пакет находится в разработке, не рекомендуется к использованию в production.

## Установка и использование

Перед тем, как использовать библиотеку логгера необходимо создать таблицу в вашей MySQL БД:

```mysql
create table table_name
(
    id       int auto_increment primary key,
    datetime datetime default CURRENT_TIMESTAMP not null,
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
[mysql]
host = localhost
port = 3306
user = ivanlut
password = passwd
database = logs

[file]
directory =
filename = log.txt

[service]
name = my-awesome-project

[output]
console = debug
mysql = warning
file = info
```

*Пустой параметр `directory` означает, что файл с логами будет сохранен в корне вашего проекта. Вы также можете указать
любой другой путь.*

Импортируйте класс логгера из библиотеки:

```python
from pchelog import DatabaseFileLogger

log = DatabaseFileLogger('logger.ini')
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
- [ ] вывод в Slack Workflow Webhook
- [ ] логи в отдельном файле с timestamp `log-timestamp.txt`
