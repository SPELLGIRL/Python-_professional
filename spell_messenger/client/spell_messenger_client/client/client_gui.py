#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import os

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QSize, QMetaObject, QRect, pyqtSlot, Qt, \
    QCoreApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, \
    QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QListView, QMenuBar, QMenu, QStatusBar, QAction, \
    QTextEdit, QWidget, QMainWindow, qApp, QMessageBox, QDialog, QPushButton, \
    QLineEdit, QLabel, QComboBox, QFileDialog, QHBoxLayout, QDesktopWidget

from jim.utils import Message
from .exceptions import ServerError
from .settings import STATIC


class UiMainClientWindow(object):
    """
    Класс, создающий интерфейс главного окна.
    """
    def __init__(self, main_client_window):
        main_client_window.setObjectName("MainClientWindow")
        main_client_window.resize(756, 534)
        main_client_window.setMinimumSize(QSize(756, 534))
        self.centralwidget = QWidget(main_client_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label_contacts = QLabel(self.centralwidget)
        self.label_contacts.setGeometry(QRect(10, 0, 101, 16))
        self.label_contacts.setObjectName("label_contacts")
        self.btn_add_contact = QPushButton(self.centralwidget)
        self.btn_add_contact.setGeometry(QRect(10, 450, 121, 31))
        self.btn_add_contact.setObjectName("btn_add_contact")
        self.btn_remove_contact = QPushButton(self.centralwidget)
        self.btn_remove_contact.setGeometry(QRect(140, 450, 121, 31))
        self.btn_remove_contact.setObjectName("btn_remove_contact")
        self.label_history = QLabel(self.centralwidget)
        self.label_history.setGeometry(QRect(300, 0, 391, 21))
        self.label_history.setObjectName("label_history")
        self.text_message = QTextEdit(self.centralwidget)
        self.text_message.setGeometry(QRect(300, 360, 441, 71))
        self.text_message.setObjectName("text_message")
        self.label_new_message = QLabel(self.centralwidget)
        self.label_new_message.setGeometry(QRect(300, 270, 450, 76))
        self.label_new_message.setObjectName("label_new_message")
        self.text_menu = QMenuBar(self.label_new_message)
        self.text_menu.move(0, 51)
        self.action_bold = QAction(QIcon(os.path.join(STATIC, 'img/b.jpg')),
                                   'Bold', self.text_message)
        self.action_italic = QAction(QIcon(os.path.join(STATIC, 'img/i.jpg')),
                                     'Italic', self.text_message)
        self.action_underlined = QAction(
            QIcon(os.path.join(STATIC, 'img/u.jpg')), 'Underlined',
            self.text_message)
        self.action_smile = QAction(
            QIcon(os.path.join(STATIC, 'img/smile.gif')), 'smile',
            self.text_message)
        self.list_contacts = QListView(self.centralwidget)
        self.list_contacts.setGeometry(QRect(10, 20, 251, 411))
        self.list_contacts.setObjectName("list_contacts")
        self.list_messages = QListView(self.centralwidget)
        self.list_messages.setGeometry(QRect(300, 20, 441, 271))
        self.list_messages.setObjectName("list_messages")
        self.btn_send = QPushButton(self.centralwidget)
        self.btn_send.setGeometry(QRect(610, 450, 131, 31))
        self.btn_send.setObjectName("btn_send")
        self.btn_clear = QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QRect(460, 450, 131, 31))
        self.btn_clear.setObjectName("btn_clear")
        main_client_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(main_client_window)
        self.menubar.setGeometry(QRect(0, 0, 756, 21))
        self.menubar.setObjectName("menubar")
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName("file")
        self.menu_contacts = QMenu(self.menubar)
        self.menu_contacts.setObjectName("contacts")
        self.menu_profile = QMenu(self.menubar)
        self.menu_profile.setObjectName("profile")
        main_client_window.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(main_client_window)
        self.statusBar.setObjectName("statusBar")
        main_client_window.setStatusBar(self.statusBar)
        self.menu_exit = QAction(main_client_window)
        self.menu_exit.setObjectName("menu_exit")
        self.menu_add_contact = QAction(main_client_window)
        self.menu_add_contact.setObjectName("menu_add_contact")
        self.menu_del_contact = QAction(main_client_window)
        self.menu_del_contact.setObjectName("menu_del_contact")
        self.menu_file.addAction(self.menu_exit)
        self.menu_contacts.addAction(self.menu_add_contact)
        self.menu_contacts.addAction(self.menu_del_contact)
        self.menu_contacts.addSeparator()
        self.menu_profile_avatar = QAction(main_client_window)
        self.menu_profile_avatar.setObjectName("menu_profile_avatar")
        self.menu_profile.addAction(self.menu_profile_avatar)
        self.menu_profile.addSeparator()
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_contacts.menuAction())
        self.menubar.addAction(self.menu_profile.menuAction())
        self.retranslate_ui(main_client_window)
        self.btn_clear.clicked.connect(self.text_message.clear)
        QMetaObject.connectSlotsByName(main_client_window)

    def retranslate_ui(self, main_client_window):
        _translate = QCoreApplication.translate
        main_client_window.setWindowTitle(
            _translate("MainClientWindow", "Чат Программа alpha release"))
        self.label_contacts.setText(
            _translate("MainClientWindow", "Список контактов:"))
        self.btn_add_contact.setText(
            _translate("MainClientWindow", "Добавить контакт"))
        self.btn_remove_contact.setText(
            _translate("MainClientWindow", "Удалить контакт"))
        self.label_history.setText(
            _translate("MainClientWindow", "История сообщений:"))
        self.label_new_message.setText(
            _translate("MainClientWindow", "Введите новое сообщение:"))
        self.btn_send.setText(
            _translate("MainClientWindow", "Отправить сообщение"))
        self.btn_clear.setText(_translate("MainClientWindow", "Очистить поле"))
        self.menu_file.setTitle(_translate("MainClientWindow", "Файл"))
        self.menu_contacts.setTitle(_translate("MainClientWindow", "Контакты"))
        self.menu_profile.setTitle(_translate("MainClientWindow", "Профиль"))
        self.menu_exit.setText(_translate("MainClientWindow", "Выход"))
        self.menu_profile_avatar.setText(
            _translate("MainClientWindow", "Аватар"))
        self.menu_add_contact.setText(
            _translate("MainClientWindow", "Добавить контакт"))
        self.menu_del_contact.setText(
            _translate("MainClientWindow", "Удалить контакт"))


class ClientMainWindow(QMainWindow):
    """
    Класс - основное окно пользователя.
    Содержит всю основную логику работы клиентского модуля.
    """
    def __init__(self, database, transport):
        super().__init__()
        # основные переменные
        self.database = database
        self.transport = transport

        # Загружаем конфигурацию окна
        self.ui = UiMainClientWindow(self)

        self.select_dialog = None
        self.remove_dialog = None
        self.avatar_window = None

        # Кнопка "Выход"
        self.ui.menu_exit.triggered.connect(qApp.exit)

        # Кнопка отправить сообщение
        self.ui.btn_send.clicked.connect(self.send_message)

        # "Аватар пользователя"
        self.ui.menu_profile_avatar.triggered.connect(
            self.profile_avatar_window)

        # "добавить контакт"
        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_window)

        # Удалить контакт
        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.ui.menu_del_contact.triggered.connect(self.delete_contact_window)

        # Меню форматирования сообщения
        self.ui.action_bold.triggered.connect(self.action_bold)
        self.ui.action_italic.triggered.connect(self.action_italic)
        self.ui.action_underlined.triggered.connect(self.action_underlined)
        self.ui.action_smile.triggered.connect(
            lambda: self.action_smile('img/smile.gif'))
        self.ui.text_menu.addAction(self.ui.action_bold)
        self.ui.text_menu.addAction(self.ui.action_italic)
        self.ui.text_menu.addAction(self.ui.action_underlined)
        self.ui.text_menu.addAction(self.ui.action_smile)

        # Дополнительные требующиеся атрибуты
        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.current_chat_key = None
        self.encryptor = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)

        # Даблклик по листу контактов отправляется в обработчик
        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)

        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self):
        """
        Метод делающий поля ввода неактивными.
        :return:
        """
        # Надпись  - получатель.
        self.ui.label_new_message.setText(
            'Для выбора получателя дважды кликните на нем в окне контактов.')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        # Поле ввода и кнопка отправки неактивны до выбора получателя.
        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)

    def history_list_update(self):
        """
        Метод заполняющий соответствующий QListView
        историей переписки с текущим собеседником.
        :return:
        """
        # Получаем историю сортированную по дате
        sorted_list = sorted(self.database.get_history(self.current_chat),
                             key=lambda item: item[3])
        # Если модель не создана, создадим.
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)
        # Очистим от старых записей
        self.history_model.clear()
        # Берём не более 20 последних записей.
        length = len(sorted_list)
        start_index = 0
        if length > 20:
            start_index = length - 20
        # Заполнение модели записями, так-же стоит разделить входящие
        # и исходящие выравниванием и разным фоном.
        # Записи в обратном порядке, поэтому выбираем их с конца и не более 20
        for i in range(start_index, length):
            item = sorted_list[i]
            if item[1] == 'in':
                mess = QStandardItem(
                    f'Входящее от '
                    f'{item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess)
            else:
                mess = QStandardItem(
                    f'Исходящее от '
                    f'{item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setTextAlignment(Qt.AlignRight)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
                self.history_model.appendRow(mess)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        """
        Метод обработчик события двойного клика по списку контактов.
        :return:
        """
        # Выбранный пользователем (даблклик) находится
        # в выделеном элементе в QListView
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        # вызываем основную функцию
        self.set_active_user()

    def set_active_user(self):
        """
        Метод активации чата с собеседником.
        :return:
        """
        # Запрашиваем публичный ключ пользователя и создаём объект шифрования
        try:
            self.current_chat_key = self.transport.key_request(
                self.current_chat)
            if self.current_chat_key:
                self.encryptor = PKCS1_OAEP.new(
                    RSA.import_key(self.current_chat_key))
        except (OSError):
            self.current_chat_key = None
            self.encryptor = None

        # Если ключа нет то ошибка, что не удалось начать чат с пользователем
        if not self.current_chat_key:
            self.messages.warning(
                self, 'Ошибка',
                'Для выбранного пользователя нет ключа шифрования.')
            return

        # Ставим надпись и активируем кнопки
        self.ui.label_new_message.setText(
            f'Введите сообщенние для {self.current_chat}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)

        # Заполняем окно историю сообщений по требуемому пользователю.
        self.history_list_update()

    def clients_list_update(self):
        """
        Метод обновляющий список контактов.
        :return:
        """
        contacts_list = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def profile_avatar_window(self):
        self.avatar_window = AvatarWindow(self)
        img_folder = os.path.join(STATIC, 'avatars')
        if not os.path.exists(img_folder):
            os.mkdir(img_folder)
        self.avatar_window.show()

    def add_contact_window(self):
        """
        Метод создающий окно - диалог добавления контакта.
        :return:
        """
        self.select_dialog = AddContactDialog(self.transport, self.database)
        self.select_dialog.btn_ok.clicked.connect(
            lambda: self.add_contact_action(self.select_dialog))
        self.select_dialog.show()

    def add_contact_action(self, item):
        """
        Метод обработчк нажатия кнопки "Добавить.
        :param item:
        :return:
        """
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact):
        """
        Метод добавляющий контакт в серверную и клиентсткую BD.
        После обновления баз данных обновляет и содержимое окна.
        :param new_contact:
        :return:
        """
        try:
            self.transport.add_contact(new_contact)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка',
                                       'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.add_contact(new_contact)
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)
            # logger.info(f'Успешно добавлен контакт {new_contact}')
            self.messages.information(self, 'Успех',
                                      'Контакт успешно добавлен.')

    def delete_contact_window(self):
        """
        Метод создающий окно удаления контакта.
        :return:
        """
        self.remove_dialog = DelContactDialog(self.database)
        self.remove_dialog.btn_ok.clicked.connect(
            lambda: self.delete_contact(self.remove_dialog))
        self.remove_dialog.show()

    def delete_contact(self, item):
        """
        Метод удаляющий контакт из серверной и клиентсткой BD.
        После обновления баз данных обновляет и содержимое окна.
        :param item: Выбранный контакт.
        :return:
        """
        selected = item.selector.currentText()
        try:
            self.transport.remove_contact(selected)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка',
                                       'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.del_contact(selected)
            self.clients_list_update()
            # logger.info(f'Успешно удалён контакт {selected}')
            self.messages.information(self, 'Успех', 'Контакт успешно удалён.')
            item.close()
            # Если удалён активный пользователь, то деактивируем поля ввода.
            if selected == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def send_message(self):
        """
        Метод отправки сообщения текущему собеседнику.
        Реализует шифрование сообщения и его отправку.
        :return:
        """
        # Текст в поле, проверяем что поле не пустое,
        # затем забирается сообщение и поле очищается
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return
        message_text_encrypted = self.encryptor.encrypt(
            message_text.encode('utf8'))
        message_text_encrypted_base64 = base64.b64encode(
            message_text_encrypted)
        try:
            self.transport.send_message(
                self.current_chat,
                message_text_encrypted_base64.decode('ascii'))
        except ServerError as err:
            self.messages.critical(self, 'Ошибка', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка',
                                       'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(self, 'Ошибка',
                                   'Потеряно соединение с сервером!')
            self.close()
        else:
            if self.current_chat != self.transport.user_name:
                self.database.save_message(self.current_chat, "out",
                                           message_text)
            self.history_list_update()

    def action_bold(self):
        """Метод изменения вводимого текста на жирный"""
        myFont = QFont()
        myFont.setBold(True)
        self.ui.text_message.setFont(myFont)

    def action_italic(self):
        """Метод изменения вводимого текста на курсив """
        myFont = QFont()
        myFont.setItalic(True)
        self.ui.text_message.setFont(myFont)

    def action_underlined(self):
        """Метод изменения вводимого текста на подчёркнутый"""
        myFont = QFont()
        myFont.setUnderline(True)
        self.ui.text_message.setFont(myFont)

    def action_smile(self, url):
        self.ui.text_message.textCursor().insertHtml(
            f'<img src="{os.path.join(STATIC, url)}" />')

    # Слот приёма нового сообщений
    @pyqtSlot(Message)
    def message(self, message: Message):
        """
        Слот обработчик поступаемых сообщений, выполняет дешифровку
        поступаемых сообщений и их сохранение в истории сообщений.
        Запрашивает пользователя если пришло сообщение не от текущего
        собеседника. При необходимости меняет собеседника.
        :param message: Полученное сообщение
        :return:
        """
        sender = message.sender
        # Получаем строку байтов
        encrypted_message = base64.b64decode(message.text)
        # Декодируем строку, при ошибке выдаём сообщение и завершаем функцию
        try:
            decrypted_message = self.transport.decrypter.decrypt(
                encrypted_message)
        except (ValueError, TypeError):
            self.messages.warning(self, 'Ошибка',
                                  'Не удалось декодировать сообщение.')
            return
        # Сохраняем сообщение в базу и обновляем историю сообщений
        # или открываем новый чат.
        self.database.save_message(sender, 'in',
                                   decrypted_message.decode('utf8'))
        if sender == self.current_chat:
            self.history_list_update()
        else:
            # Проверим есть ли такой пользователь у нас в контактах:
            if self.database.check_contact(sender):
                # Если есть, спрашиваем и желании открыть с ним чат
                # и открываем при желании
                if self.messages.question(
                        self, 'Новое сообщение',
                        f'Получено новое сообщение от '
                        f'{sender}, открыть чат с ним?', QMessageBox.Yes,
                        QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.set_active_user()
            else:
                # Раз нету,спрашиваем хотим ли добавить юзера в контакты.
                if self.messages.question(
                        self, 'Новое сообщение',
                        f'Получено новое сообщение от '
                        f'{sender}.\n Данного пользователя нет в '
                        f'вашем контакт-листе.\n '
                        f'Добавить в контакты и открыть чат с ним?',
                        QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self):
        """
        Слот обработчик потери соеднинения с сервером.
        Выдаёт окно предупреждение и завершает работу приложения.
        :return:
        """
        self.messages.warning(self, 'Сбой соединения',
                              'Потеряно соединение с сервером. ')
        self.close()

    def make_connection(self, trans_obj):
        """
        Метод обеспечивающий соединение сигналов и слотов.
        :param trans_obj:
        :return:
        """
        trans_obj.new_message.connect(self.message)
        trans_obj.connection_lost.connect(self.connection_lost)


class AvatarWindow(QWidget):
    """Класс - окно сохранения аватара пользователя."""
    def __init__(self, parent):
        super().__init__(parent, Qt.Window)
        self.main = parent
        self.width = 400
        self.height = 400
        self.filtering_image = None
        self.current_image = None
        self.h_box = QHBoxLayout(self)
        self.label = QLabel(self)

        self.init_ui()

    def init_ui(self):
        self.h_box.addWidget(self.label)
        self.setLayout(self.h_box)

        # Меню
        menu_bar = QMenuBar(self)
        menu_bar.setFixedWidth(self.width)
        file_menu = menu_bar.addMenu('Файл')
        filter_menu = menu_bar.addMenu('Фильтр')

        # Открыть файл
        open_file = QAction(QIcon('open.png'), 'Открыть...', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Открыть файл')
        open_file.triggered.connect(self.open_dialog)
        file_menu.addAction(open_file)

        # Сохранить файл
        save_file = QAction(QIcon('save.png'), 'Сохранить', self)
        save_file.setShortcut('Ctrl+S')
        save_file.setStatusTip('Сохранить файл')
        save_file.triggered.connect(self.save_dialog)
        file_menu.addAction(save_file)

        # Выйти
        close_action = QAction(QIcon('exit.png'), 'Закрыть', self)
        close_action.setShortcut('Ctrl+Q')
        close_action.setStatusTip('Закрыть')
        close_action.triggered.connect(lambda: self.close_window())
        file_menu.addAction(close_action)

        # Фильтры
        # Оттенки серого
        gray_action = QAction(QIcon('gray.png'), 'Grey', self)
        gray_action.setStatusTip('Оттенки серого')
        gray_action.triggered.connect(lambda: self.process_filter('grey'))
        filter_menu.addAction(gray_action)

        # ЧБ
        bw_action = QAction(QIcon('bw.png'), 'BW', self)
        bw_action.setStatusTip('ЧБ')
        bw_action.triggered.connect(lambda: self.process_filter('bw'))
        filter_menu.addAction(bw_action)

        # Негатив
        negative_action = QAction(QIcon('negative.png'), 'Negative', self)
        negative_action.setStatusTip('Обратные цвета')
        negative_action.triggered.connect(
            lambda: self.process_filter('negative'))
        filter_menu.addAction(negative_action)

        # Сепия
        sepia_action = QAction(QIcon('sepia.png'), 'Sepia', self)
        sepia_action.setStatusTip('Сепия')
        sepia_action.triggered.connect(lambda: self.process_filter('sepia'))
        filter_menu.addAction(sepia_action)

        # Оригинал
        original_action = QAction(QIcon('original.png'), 'Original', self)
        original_action.setStatusTip('Оригинал')
        original_action.triggered.connect(lambda: self.return_original_image())
        filter_menu.addAction(original_action)

        self.set_geometry()
        self.setWindowTitle('Установка аватара')

        user = self.main.database.get_user_by_name(
            self.main.transport.user_name)
        if user and user.avatar:
            image_path = os.path.join(STATIC, user.avatar)
            if os.path.exists(image_path):
                image = Image.open(image_path)
                self.filtering_image = ProcessingImage(image)
                self.current_image = self.filtering_image
                self.reload_image(self.filtering_image)

    def close_window(self):
        self.close()

    def set_geometry(self):
        desktop = QDesktopWidget().availableGeometry()
        left = int((desktop.width() - self.width) / 2)
        top = int((desktop.height() - self.height) / 2)
        self.setGeometry(0, 0, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.move(left, top)

    def resize_crop(self, image):
        """
        Метод, масштабирующий и обрезающий изображение
        :param image: Входное изображение
        :return: Отредактированное изображение
        """
        # Изменение размера до допустимого максимума
        old_size = image.size
        ratio = float(self.width) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        image = image.resize(new_size, Image.ANTIALIAS)
        # Обрезка до квадратного
        image = image.crop((0, 0, min(new_size), min(new_size)))
        return image

    def reload_image(self, file_path):
        """Метод, обновляющий изображение в окне"""
        image = ImageQt(file_path.to_qt())
        pix_map = QPixmap.fromImage(image)
        self.label.resize(self.width, self.height)
        if pix_map.width() > self.width or pix_map.height() > self.height:
            pix_map = pix_map.scaled(self.width - 25, self.height - 25,
                                     Qt.KeepAspectRatio)
        if pix_map.width() <= self.width:
            self.label.move((self.width - pix_map.width()) / 2, 0)
        self.label.setPixmap(pix_map)

    def open_dialog(self):
        """Метод, описывающий логику окна открытия изображения"""
        file_path = QFileDialog.getOpenFileName(self, 'Открыть файл')[0]
        if file_path:
            image = Image.open(file_path)
            self.filtering_image = ProcessingImage(image)
            self.current_image = self.filtering_image
            self.reload_image(self.filtering_image)

    def save_dialog(self):
        """Метод, описывающий логику кнопки сохранения изображения"""
        if self.current_image:
            image = self.resize_crop(self.current_image.image)
            img_path = f'avatars/{self.main.transport.user_name}.jpg'
            image.save(os.path.join(STATIC, img_path))
            self.main.database.save_avatar(img_path)

    def return_original_image(self):
        """Метод, возвращающий исходное изображение"""
        if self.filtering_image:
            self.current_image = self.filtering_image
            self.reload_image(self.filtering_image)

    def process_filter(self, filter_name):
        """
        Метод, запускающий обработку изображения
        :param filter_name: Название фильтра
        :return: Отредактированное изображение
        """
        if self.filtering_image:
            filter_method = getattr(self.filtering_image, filter_name)
            result = filter_method()
            self.current_image = result
            self.reload_image(result)


class ProcessingImage:
    """Класс для обработки изображения"""
    def __init__(self, image):
        self.image = image.copy()
        self.draw = ImageDraw.Draw(self.image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pix = self.image.load()

    def to_qt(self):
        return self.image.convert('RGBA')

    def grey(self):
        """Метод, применябщий фильтр оттенков серого"""
        new_image = ProcessingImage(self.image)
        for i in range(new_image.width):
            for j in range(new_image.height):
                a = new_image.pix[i, j][0]
                b = new_image.pix[i, j][1]
                c = new_image.pix[i, j][2]
                S = (a + b + c) // 3
                new_image.draw.point((i, j), (S, S, S))
        return new_image

    def bw(self):
        """Метод, применябщий черно-белый фильтр"""
        new_image = ProcessingImage(self.image)
        factor = 50
        for i in range(new_image.width):
            for j in range(new_image.height):
                a = new_image.pix[i, j][0]
                b = new_image.pix[i, j][1]
                c = new_image.pix[i, j][2]
                s = a + b + c
                if s > (((255 + factor) // 2) * 3):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                new_image.draw.point((i, j), (a, b, c))
        return new_image

    def negative(self):
        """Метод, применябщий фильтр инверсии"""
        new_image = ProcessingImage(self.image)
        for i in range(new_image.width):
            for j in range(new_image.height):
                a = new_image.pix[i, j][0]
                b = new_image.pix[i, j][1]
                c = new_image.pix[i, j][2]
                new_image.draw.point((i, j), (255 - a, 255 - b, 255 - c))
        return new_image

    def sepia(self):
        """Метод, применябщий фильтр сепия"""
        new_image = ProcessingImage(self.image)
        depth = 30
        for i in range(new_image.width):
            for j in range(new_image.height):
                a = new_image.pix[i, j][0]
                b = new_image.pix[i, j][1]
                c = new_image.pix[i, j][2]
                S = (a + b + c)
                a = S + depth * 2
                b = S + depth
                c = S
                if a > 255:
                    a = 255
                if b > 255:
                    b = 255
                if c > 255:
                    c = 255
                new_image.draw.point((i, j), (a, b, c))
        return new_image


class UserNameDialog(QDialog):
    """
    Класс реализующий стартовый диалог с запросом логина и пароля
    пользователя.
    """
    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        self.setWindowTitle('Привет!')
        self.setFixedSize(175, 135)

        self.label = QLabel('Введите имя пользователя:', self)
        self.label.move(10, 10)
        self.label.setFixedSize(150, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 30)

        self.btn_ok = QPushButton('Начать', self)
        self.btn_ok.move(10, 105)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 105)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.label_passwd = QLabel('Введите пароль:', self)
        self.label_passwd.move(10, 55)
        self.label_passwd.setFixedSize(150, 15)

        self.client_passwd = QLineEdit(self)
        self.client_passwd.setFixedSize(154, 20)
        self.client_passwd.move(10, 75)
        self.client_passwd.setEchoMode(QLineEdit.Password)

        self.show()

    def click(self):
        """
        Метод обрабтчик кнопки ОК, если поле вводе не пустое,
        ставим флаг и завершаем приложение.
        :return:
        """
        if self.client_name.text():
            self.ok_pressed = True
            qApp.exit()


class AddContactDialog(QDialog):
    """
    Диалог добавления пользователя в список контактов.
    Предлагает пользователю список возможных контактов и
    добавляет выбранный в контакты.
    """
    def __init__(self, transport, database):
        super().__init__()
        self.transport = transport
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для добавления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для добавления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Обновить список', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        # Заполняем список возможных контактов
        self.update_possible_contacts()
        # Назначаем действие на кнопку обновить
        self.btn_refresh.clicked.connect(self.update_possible_contacts)

    def possible_contacts_update(self):
        """
        Метод заполнения списка возможных контактов.
        Создаёт список всех зарегистрированных пользователей
        за исключением уже добавленных в контакты и самого себя.
        :return:
        """
        self.selector.clear()
        # множества всех контактов и контактов клиента
        contacts_list = set(self.database.get_contacts())
        users_list = set(self.database.get_connected())
        # Удалим сами себя из списка пользователей,
        # чтобы нельзя было добавить самого себя
        users_list.remove(self.transport.user_name)
        # Добавляем список возможных контактов
        self.selector.addItems(users_list - contacts_list)

    def update_possible_contacts(self):
        """
        Метод обновления списка возможных контактов. Запрашивает с сервера
        список известных пользователей и обновляет содержимое окна.
        :return:
        """
        try:
            self.transport.user_list_update()
        except OSError:
            pass
        else:
            self.possible_contacts_update()


class DelContactDialog(QDialog):
    """
    Диалог удаления контакта. Прделагает текущий список контактов,
    не имеет обработчиков для действий.
    """
    def __init__(self, database):
        super().__init__()
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для удаления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для удаления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_ok = QPushButton('Удалить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        # заполнитель контактов для удаления
        self.selector.addItems(sorted(self.database.get_contacts()))
