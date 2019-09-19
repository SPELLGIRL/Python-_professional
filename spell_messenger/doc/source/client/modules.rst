Client package
==============

Клиентское приложение для обмена сообщениями. Поддерживает
отправку сообщений пользователям которые находятся в сети, сообщения шифруются
с помощью алгоритма RSA с длинной ключа 2048 bit.

Использование

* ``python spell_messenger_client {адрес сервера} {порт}``
* ``python spell_messenger_client/__main__.py {адрес сервера} {порт}``
* ``python spell_messenger_client/main.py {адрес сервера} {порт}``

Поддерживает аргументы коммандной строки:

1. {имя сервера} - IP адрес сервера.
2. {порт} - порт сервера.
3. -u или --user - имя пользователя с которым произойдёт вход в систему.
4. -p или --password - пароль пользователя.
5. -m или --mode - режим запуска (gui/console), по умолчанию gui
6. -db или --database - Выбор БД (SQLite/mongoDB), по умолчанию SQLite.

Все опции командной строки являются необязательными, но имя пользователя и
пароль необходимо использовать в паре.

Примеры использования:

* ``python spell_messenger_client``

*Запуск приложения с параметрами по умолчанию.*

* ``python spell_messenger_client ip_address some_port``

*Запуск приложения с подключением к серверу по адресу ip_address:port*

* ``python spell_messenger_client -u test1 -p 123``

*Запуск приложения с пользователем test1 и паролем 123*

* ``python spell_messenger_client ip_address some_port -u test1 -p 123``

*Запуск приложения с пользователем test1 и паролем 123 и с подключением к
серверу по адресу ip_address:port*

* ``python spell_messenger_client -m console``

*Запуск приложения с настройками по умолчанию без графической оболочки*

``python spell_messenger_client -db mongo``

*Запуск с настройками по умолчанию с MongoDB вместо SQLite*

.. toctree::
   :maxdepth: 2

   main
   client
   client_gui
   handlers
   decorators
   descriptors
   metaclasses
   exceptions
   db
   jim
   log
   settings
