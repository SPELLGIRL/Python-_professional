Server package
==============

Серверный пакет мессенджера. Обрабатывает словари - сообщения,
хранит публичные ключи клиентов.

Использование

* ``python spell_messenger_server``
* ``python spell_messenger_server/__main__.py``
* ``python spell_messenger_server/main.py``

Модуль подерживает аргементы командной строки:

1. -p - Порт на котором принимаются соединения.
2. -a - Адрес прослушиваемого интерфейса.
3. -m - Выбор режима запуска (gui/console), по умолчанию gui.

Примеры использования:

``python spell_messenger_server -p 8080``

*Запуск сервера на порту 8080*

``python spell_messenger_server -a localhost``

*Запуск сервера принимающего только соединения с localhost*

``python spell_messenger_server -m console``

*Запуск с настройками по умолчанию без графической оболочки*

.. toctree::
   :maxdepth: 2

   main
   server
   server_gui
   handlers
   decorators
   descriptors
   metaclasses
   db
   jim
   log
   settings
