#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Модуль, описывающий работу с БД"""

import os

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker

from client.settings import DATABASE
from .models import Base, Contact, MessageHistory, ConnectedUser, User


class Repository:
    """
    Класс - оболочка для работы с базой данных клиента.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется декларативный подход.
    """
    def __init__(self, name):
        self.user_name = name
        if not os.path.exists(DATABASE):
            os.mkdir(DATABASE)
        self.engine = create_engine(
            f'sqlite:///{os.path.join(DATABASE, f"client_{name}.db")}',
            echo=False,
            pool_recycle=7200,
            connect_args={'check_same_thread': False})

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)

        self.session = Session()

    def add_contact(self, user_name: str):
        """
        Метод добавляющий контакт в базу данных.
        :param user_name: Имя контакта
        :return:
        """
        if not self.session.query(
                exists().where(Contact.name == user_name)).scalar():
            contact = Contact(user_name)
            self.session.add(contact)
            self.session.commit()
            return contact

    def add_client(self, user_name: str):
        """
        Метод добавляющий подключённого клиента в базу данных.
        :param user_name: Имя клиента
        :return:
        """
        if not self.session.query(
                exists().where(ConnectedUser.name == user_name)).scalar():
            contact = ConnectedUser(user_name)
            self.session.add(contact)
            self.session.commit()
            return contact

    def del_contact(self, user_name: str):
        """
        Метод удаляющий определённый контакт.
        :param user_name: Имя контакта
        :return:
        """
        self.session.query(Contact).filter_by(name=user_name).delete()
        self.session.commit()

    def clear_contacts(self):
        """
        Метод очищает локальный список контактов.
        :return:
        """
        self.session.query(Contact).delete()
        self.session.query(ConnectedUser).delete()
        self.session.commit()

    def save_message(self, contact: str, direction: str, message: str):
        """
        Метод сохраняющий сообщение в базе данных.
        :param contact: Имя отправителя.
        :param direction: Направление.
        :param message: Текст сообщения.
        :return:
        """
        message_row = MessageHistory(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    def get_user_by_name(self, name: str):
        """
        Метод получения объекта пользователя по его имени.
        :param name: Имя клиента
        :return: Объект клиента
        """
        user = self.session.query(User).filter(User.name == name)
        return user.first() if user.count() else None

    def add_user(self):
        """
        Метод добавления пользователя.
        Создаёт запись в таблице входивших пользователей.
        :return:
        """
        user = self.get_user_by_name(self.user_name)
        if not user:
            user = User(self.user_name)
            self.session.add(user)
            self.session.commit()
        return user

    def save_avatar(self, img_path):
        """
        Метод добавления аватара пользователя.
        :param img_path: Путь к изображению
        :return:
        """
        user = self.get_user_by_name(self.user_name)
        if user:
            user.avatar = img_path
            self.session.add(user)
            self.session.commit()

    def get_history(self, contact=None) -> list:
        """
        Метод возвращающий историю сообщений с определённым пользователем.
        :param contact: Имя контакта
        :return:
        """
        query = self.session.query(MessageHistory)
        if contact:
            query = query.filter_by(contact=contact)
        return [(history_row.contact, history_row.direction,
                 history_row.message, history_row.time)
                for history_row in query.all()]

    def get_contacts(self) -> list:
        """
        Метод возвращающий список всех контактов.
        :return:
        """
        query = self.session.query(Contact.name).all()
        return [value for (value, ) in query]

    def get_connected(self, search=None) -> list:
        """
        Метод возвращающий список подключённых пользователей.
        :return:
        """
        if search:
            search = f'%{search}%'
            query = self.session.query(ConnectedUser.name).filter(
                ConnectedUser.name.like(search)).all()
        else:
            query = self.session.query(ConnectedUser.name).all()
        return [value for (value, ) in query]

    def check_contact(self, contact: str) -> bool:
        """
        Метод проверяющий существует ли контакт.
        :param contact: Имя контакта
        :return:
        """
        if self.session.query(Contact).filter_by(name=contact).count():
            return True
        else:
            return False
