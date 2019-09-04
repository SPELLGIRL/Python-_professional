#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Модуль, описывающий работу с БД"""

import datetime
import os

from pymongo import MongoClient
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from server.settings import DATABASE
from .models import Base, User, History, contact_table


class Repository:
    """
    Класс - оболочка для работы с базой данных сервера.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется декларативный подход.
    """
    def __init__(self, path=None, name=None):
        if not path:
            path = DATABASE
            if not os.path.exists(path):
                os.mkdir(path)
        if not name:
            name = "server.db"
        self.engine = create_engine(f'sqlite:///{os.path.join(path, name)}',
                                    echo=False,
                                    pool_recycle=7200,
                                    connect_args={'check_same_thread': False})

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)

        self.session = Session()
        self.new_connection = True

    def user_login(self, user_name: str, ip: str, key: str):
        """
        Метод выполняющийся при входе пользователя,
        записывает в базу факт входа.
        Обновляет открытый ключ пользователя при его изменении.
        :param user_name: Имя клиента
        :param ip: IP клиента
        :param key: Публичный ключ клиента
        :return:
        """
        user = self.get_user_by_name(user_name)
        if user:
            user.is_online = True
            user.last_login = datetime.datetime.now()
            if user.pubkey != key:
                user.pubkey = key
            self.add_login_history(user, ip)
            self.session.commit()
        else:
            raise ValueError('Пользователь не зарегистрирован.')

    def user_logout(self, user_name: str):
        """
        Метод фиксирующий отключения пользователя.
        :param user_name: Имя клиента
        :return:
        """
        user = self.get_user_by_name(user_name)
        if user:
            user.is_online = False
            self.session.commit()

    def add_user(self, user_name: str, password: str = None):
        """
        Метод регистрации пользователя.
        Принимает имя и хэш пароля, создаёт запись в таблице статистики.
        :param user_name: Имя клиента
        :param password: Хэш пароля клиента
        :return:
        """
        user = self.get_user_by_name(user_name)
        if not user:
            user = User(user_name, password)
            self.session.add(user)
            self.session.commit()
        return user

    def remove_user(self, user_name: str):
        """
        Метод удаляющий пользователя из базы.
        :param user_name: Имя клиента
        :return:
        """
        user = self.get_user_by_name(user_name)
        if user:
            self.session.query(User).filter_by(id=user.id).delete()
            self.session.query(History).filter_by(user_id=user.id).delete()
            contacts = self.session.query(contact_table).filter(
                or_(contact_table.c.user_id == user.id,
                    contact_table.c.contact_id == user.id))
            contacts.delete(synchronize_session=False)
            self.session.commit()

    def add_login_history(self, user, ip: str):
        """
        Метод, добавляюший запись в таблицу истории.
        :param user: Объект клиента
        :param ip: IP клиента
        :return:
        """
        history = History(user, ip)
        self.session.add(history)
        self.session.commit()

    def get_user_by_name(self, name: str):
        """
        Метод получения объекта клиента по его имени.
        :param name: Имя клиента
        :return: Объект клиента
        """
        user = self.session.query(User).filter(User.name == name)
        return user.first() if user.count() else None

    def get_hash(self, user_name: str):
        """
        Метод получения хэша пароля пользователя.
        :param user_name: Имя клиента
        :return:
        """
        user = self.get_user_by_name(user_name)
        return user.password if user else None

    def get_pubkey(self, user_name: str):
        """
        Метод получения публичного ключа пользователя.
        :param user_name: Имя клиента
        :return:
        """
        user = self.get_user_by_name(user_name)
        return user.pubkey

    def users_list(self, active: bool = None) -> list:
        """
        Метод возвращающий список пользователей.
        :param active: True/False/None
        :return:
        """
        query = self.session.query(User.name)
        if active is not None:
            query = query.filter(User.is_online == active)
        return [value for (value, ) in query.all()]

    def login_history(self, user_name: str = None) -> list:
        """
        Метод возвращающий историю входов.
        :param user_name: Имя клиента
        :return:
        """
        query = self.session.query(
            User.name, func.strftime('%Y-%m-%d %H:%M', History.time),
            History.ip).join(User)
        if user_name:
            query = query.filter(User.name == user_name)
        return [value for value in query.all()]

    def get_contact_list(self, user_name: str) -> list:
        """
        Метод возвращающий список контактов пользователя.
        :param user_name: Имя клиента
        :return:
        """
        user = self.get_user_by_name(user_name)
        return [contact.name for contact in user.contacts]

    def add_contact(self, user_name: str, contact_name: str):
        """
        Метод добавления контакта для пользователя.
        :param user_name: Имя клиента
        :param contact_name: Имя контакта
        :return:
        """
        user = self.get_user_by_name(user_name)
        contact = self.get_user_by_name(contact_name)
        if contact:
            user.contacts.append(contact)
            self.session.add(user)
            self.session.commit()
        else:
            raise Exception

    def remove_contact(self, user_name: str, contact_name: str):
        """
        Метод удаления контакта пользователя.
        :param user_name: Имя клиента
        :param contact_name: Имя контакта
        :return:
        """
        user = self.get_user_by_name(user_name)
        contact = self.get_user_by_name(contact_name)
        if contact:
            user.contacts.remove(contact)
            self.session.add(user)
            self.session.commit()
        else:
            raise Exception

    def process_message(self, sender, recipient):
        """
        Метод записывающий в таблицу истории факт передачи сообщения.
        :param sender: Имя отправителя
        :param recipient: Имя получателя
        :return:
        """
        sender = self.get_user_by_name(sender)
        recipient = self.get_user_by_name(recipient)
        if sender:
            sender.sent += 1
        if recipient:
            recipient.receive += 1
        self.session.commit()

    def message_history(self):
        """
        Метод возвращающий статистику сообщений.
        :return:
        """
        query = self.session.query(User.name, User.last_login, User.sent,
                                   User.receive)
        return query.all()

    def add_general_chat_history(self, user_name, text):
        pass


class MongoRepository:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.db
        self.users = self.db.users
        self.history = self.db.history
        self.contacts = self.db.contacts
        self.general_chat = self.db.general_chat
        self.new_connection = True

    def user_login(self, user_name: str, ip: str, key: str):
        user = self.get_user_by_name(user_name)
        if user:
            values = {
                "$set": {
                    'is_online':
                    True,
                    'last_login':
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            }
            self.users.update_one(user, values)
            if user.get('pubkey') != key:
                values = {"$set": {'pubkey': key}}
                self.users.update_one(user, values)
            self.add_login_history(user, ip)
        else:
            raise ValueError('Пользователь не зарегистрирован.')

    def user_logout(self, user_name: str):
        user = self.get_user_by_name(user_name)
        if user:
            values = {"$set": {'is_online': False}}
            self.users.update_one(user, values)

    def add_user(self, user_name: str, password: str = None):
        user = self.get_user_by_name(user_name)
        if not user:
            user = {
                'user_name': user_name,
                'sent': 0,
                'receive': 0,
                'password': password,
            }
            user = self.users.insert_one(user)
        return user

    def remove_user(self, user_name: str):
        user = self.get_user_by_name(user_name)
        if user:
            self.users.delete_one(user)
            self.history.delete_many({'user_name': user_name})
            self.contacts.delete_many({'user_name': user_name})

    def add_login_history(self, user, ip: str):
        user_name = user.get('user_name')
        self.history.insert_one({
            'user_name':
            user_name,
            'time':
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'ip':
            ip
        })

    def get_user_by_name(self, name: str):
        user = self.users.find_one({'user_name': name})
        return user if user else None

    def get_hash(self, user_name: str):
        user = self.get_user_by_name(user_name)
        return user.get('password') if user else None

    def get_pubkey(self, user_name: str):
        user = self.get_user_by_name(user_name)
        return user.get('pubkey') if user else None

    def users_list(self, active: bool = None) -> list:
        query = self.users.find()
        if active is not None:
            query = self.users.find({'is_online': active})
        return [value.get('user_name') for value in query]

    def login_history(self, user_name: str = None) -> list:
        fields = {'_id': 0, 'user_name': 1, 'time': 1, 'ip': 1}
        query = self.history.find({}, fields)
        if user_name:
            query = self.history.find({'user_name': user_name}, fields)
        return [(user.get('user_name'), user.get('time'), user.get('ip'))
                for user in query]

    def get_contact_list(self, user_name: str) -> list:
        return [
            contact.get('contact_name')
            for contact in self.contacts.find({'user_name': user_name})
        ]

    def add_contact(self, user_name: str, contact_name: str):
        contact = self.get_user_by_name(contact_name)
        if contact:
            self.contacts.insert_one({
                'user_name': user_name,
                'contact_name': contact_name
            })
        else:
            raise Exception

    def remove_contact(self, user_name: str, contact_name: str):
        contact = self.get_user_by_name(contact_name)
        if contact:
            self.contacts.delete_one({
                'user_name': user_name,
                'contact_name': contact_name
            })
        else:
            raise Exception

    def process_message(self, sender, recipient):
        sender = self.get_user_by_name(sender)
        recipient = self.get_user_by_name(recipient)
        if sender:
            s_sent = sender.get('sent')
            s_sent += 1
            self.users.update_one(sender, {"$set": {'sent': s_sent}})
        if recipient:
            r_receive = recipient.get('receive')
            r_receive += 1
            self.users.update_one(recipient, {"$set": {'receive': r_receive}})

    def message_history(self):
        query = self.users.find({}, {
            '_id': 0,
            'user_name': 1,
            'last_login': 1,
            'sent': 1,
            'receive': 1
        })
        return [(user.get('user_name'), user.get('last_login'),
                 user.get('sent'), user.get('receive')) for user in query]

    def add_general_chat_history(self, user_name, text):
        self.general_chat.insert_one({
            'user_name':
            user_name,
            'text':
            text,
            'time':
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        })
