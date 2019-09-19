#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


def set_resolution(width, height):
    min_size = 250
    if width < min_size:
        width = min_size
    if height < min_size:
        height = min_size
    return width, height


class SnakeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.win_points = 15
        self.x_snake = None
        self.y_snake = None
        self.x_min, self.x_max = self.check_size(WIDTH * .4, WIDTH), WIDTH
        self.y_min, self.y_max = self.check_size(0, HEIGHT), HEIGHT
        self.step = 20
        self.pos_apple = random.randrange(
            self.x_min + self.step, self.x_max - self.step,
            self.step), random.randrange(self.y_min + self.step,
                                         self.y_max - self.step, self.step)
        self.points = 1
        self.time = 40
        self.last_move = ''
        self.change = .105
        self.points_lbl = Label(text=f'Points :{self.points} ',
                                y=HEIGHT * .4,
                                x=-WIDTH * .4)
        self.time_label = Label(text=f'Time : {str(self.time)}',
                                y=HEIGHT * .4 + 20,
                                x=-WIDTH * .4)
        self.widget = Widget()

    def build(self):
        with self.widget.canvas:
            Color(1, 0, 0, 1)
            self.widget.apple = Rectangle(pos=(self.pos_apple[0],
                                               self.pos_apple[1]),
                                          size=(20, 20))
            Color(2, 2, 2, 1)
            self.widget.snake = Rectangle(
                pos=(random.randrange(self.x_min + self.step,
                                      self.x_max - self.step, self.step),
                     random.randrange(self.y_min + self.step,
                                      self.y_max - self.step, self.step)),
                size=(20, 20))
            Color(1, 1, 0, 1)
            self.widget.tail1 = Rectangle(pos=self.widget.snake.pos,
                                          size=(20, 20))
            for i in range(self.win_points)[1::]:
                setattr(self.widget, f'tail{i + 1}',
                        Rectangle(pos=(1000, 1000), size=(20, 20)))
            Color(0.1, 0.2, 0.5, 1)
            self.widget.bord = Rectangle(pos=(0, 0),
                                         size=(self.check_size(
                                             WIDTH * .4, WIDTH), HEIGHT + 20))

        window = FloatLayout()
        self.x_snake = self.widget.snake.pos[0]
        self.y_snake = self.widget.snake.pos[1]
        Window.bind(on_key_down=self.action)
        Clock.schedule_interval(self.move, self.change)
        Clock.schedule_interval(self.timer, 1)

        window.add_widget(self.widget)
        window.add_widget(self.time_label)
        window.add_widget(self.points_lbl)

        return window

    def move(self, dt):
        self.bump()
        self.grow()
        if self.last_move == 'Right':
            self.x_snake += self.step
            if self.x_snake > self.x_max:
                self.x_snake = self.x_min

        if self.last_move == 'Left':
            self.x_snake -= self.step
            if self.x_snake < self.x_min:
                self.x_snake = self.x_max

        if self.last_move == 'Up':
            self.y_snake += self.step
            if self.y_snake > self.y_max:
                self.y_snake = self.y_min

        if self.last_move == 'Down':
            self.y_snake -= self.step
            if self.y_snake < self.y_min:
                self.y_snake = self.y_max

        self.widget.snake.pos = self.x_snake, self.y_snake
        if self.x_snake == self.pos_apple[
                0] and self.y_snake == self.pos_apple[1]:
            self.currency()

    def timer(self, dt):
        if self.time == 0:
            self.lost()
        if self.last_move != "":
            self.time -= 1
        self.time_label.text = f'Time : {str(self.time)}'

    def currency(self):
        self.points += 1
        self.points_lbl.text = f'Points : {self.points}'
        self.time += 5
        self.pos_apple = random.randrange(
            self.x_min + self.step, self.x_max - self.step,
            self.step), random.randrange(self.y_min + self.step,
                                         self.y_max - self.step, self.step)
        self.widget.apple.pos = self.pos_apple[0], self.pos_apple[1]
        self.time_label.text = f'Time : {str(self.time)}'
        self.change -= .001

    def action(self, *args):
        args = str(args)
        args = args.split()
        if len(args) > 5:
            if (args[5] == '79,'
                    or args[5] == '7,') and self.last_move != 'Left':
                self.last_move = 'Right'
            if (args[5] == '80,'
                    or args[5] == '4,') and self.last_move != 'Right':
                self.last_move = 'Left'
            if (args[5] == '82,'
                    or args[5] == '26,') and self.last_move != 'Down':
                self.last_move = 'Up'
            if (args[5] == '81,'
                    or args[5] == '22,') and self.last_move != 'Up':
                self.last_move = 'Down'

    def grow(self):
        self.widget.tail1.pos = self.widget.snake.pos
        if self.points == self.win_points:
            self.win()
        else:
            for i in range(self.win_points)[:0:-1]:
                if self.points >= i:
                    getattr(self.widget, f'tail{i + 1}').pos = getattr(
                        self.widget, f'tail{i}').pos

    def bump(self):
        collision = [
            getattr(self.widget, f'tail{i}').pos
            for i in range(self.win_points)[1:-2]
        ]
        if self.widget.snake.pos in collision and self.points > 2:
            self.lost()

    @staticmethod
    def check_size(value, standard):
        return standard - (standard - value) // 20 * 20

    @staticmethod
    def lost():
        bt = Button(text='OK')
        bt.on_release = exit
        leave = Popup(title='You lost',
                      content=bt,
                      auto_dismiss=False,
                      size_hint=(None, None),
                      size=(WIDTH * .4, HEIGHT * .4))
        leave.open()

    @staticmethod
    def win():
        bt = Button(text='OK')
        bt.on_release = exit
        win = Popup(title='You won',
                    content=bt,
                    auto_dismiss=False,
                    size_hint=(None, None),
                    size=(WIDTH * .4, HEIGHT * .4))
        win.open()


if __name__ == '__main__':
    WIDTH, HEIGHT = set_resolution(550, 400)
    Window.size = WIDTH + 20, HEIGHT + 20
    SnakeApp.title = 'Snake'
    SnakeApp().run()
