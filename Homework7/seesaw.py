#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from random import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line


class DrawWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (random(), 1, 1)
        self.center_x = 400
        self.center_y = 300
        self.length = 300
        self.angle = 0
        self.next = True
        self.line_points = self.count_coords()
        self.my_event = None
        with self.canvas:
            Color(*self.color, mode='hsv')
            Line(points=[
                self.center_x - 100, self.center_y - 100, self.center_x + 100,
                self.center_y - 100, self.center_x, self.center_y
            ],
                 width=10,
                 close=True)
            self.line = Line(points=self.line_points, width=10)

    def on_touch_down(self, touch):
        step = self.right_down if self.next else self.left_down
        self.my_event = Clock.schedule_interval(step, 0.1)

    def on_touch_up(self, touch):
        if self.my_event:
            self.my_event.cancel()
        self.next = not self.next

    def count_coords(self):
        x1 = self.length * math.cos(self.angle) + self.center_x
        y1 = self.length * math.sin(self.angle) + self.center_y
        x2 = self.length * math.cos(self.angle + math.pi) + self.center_x
        y2 = self.length * math.sin(self.angle + math.pi) + self.center_y
        return [x1, y1, x2, y2]

    def left_down(self, obj):
        if self.line_points[3] > self.center_y - 100:
            self.angle += math.pi / 180
            self.move()

    def right_down(self, obj):
        if self.line_points[1] > self.center_y - 100:
            self.angle -= math.pi / 180
            self.move()

    def move(self):
        self.line_points = self.count_coords()
        self.line.points = self.line_points


class SeesawApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.painter = DrawWidget()

    def build(self):
        parent = Widget()
        clear_btn = Button(text='Restore')
        clear_btn.bind(on_release=self.restore)
        parent.add_widget(self.painter)
        parent.add_widget(clear_btn)
        return parent

    def restore(self, obj):
        self.painter.canvas.clear()
        self.painter.__init__()


if __name__ == '__main__':
    Window.clearcolor = (1, 1, 1, 1)
    SeesawApp().run()
