import sys

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QLabel, QHBoxLayout, QAction,
                             QFileDialog, QApplication)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filtering_image = None
        self.current_image = None
        self.width = 400
        self.height = 400
        self.h_box = QHBoxLayout(self)
        self.label = QLabel(self)

        self.init_ui()

    def init_ui(self):
        self.h_box.addWidget(self.label)
        self.setLayout(self.h_box)

        # Меню
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('Файл')
        filter_menu = menu_bar.addMenu('Фильтр')

        # Открыть файл
        open_file = QAction(QIcon('open.png'), 'Открыть...', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Открыть файл')
        open_file.triggered.connect(self.open_dialog)
        file_menu.addAction(open_file)

        # Сохранить файл
        save_file = QAction(QIcon('save.png'), 'Сохранить как...', self)
        save_file.setShortcut('Ctrl+S')
        save_file.setStatusTip('Сохранить файл')
        save_file.triggered.connect(self.save_dialog)
        file_menu.addAction(save_file)

        # Выйти
        app_exit = QAction(QIcon('exit.png'), 'Выйти', self)
        app_exit.setShortcut('Ctrl+Q')
        app_exit.setStatusTip('Выход')
        app_exit.triggered.connect(app.exit)
        file_menu.addAction(app_exit)

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
        self.setWindowTitle('Фильтр изображений')
        self.show()

    def set_geometry(self):
        left = int((app.desktop().width() - self.width) / 2)
        top = int((app.desktop().height() - self.height) / 2)
        self.setFixedSize(self.width, self.height)
        self.move(left, top)

    def reload_image(self, file_path):
        image = ImageQt(file_path.to_qt())
        pix_map = QPixmap.fromImage(image)
        self.label.resize(self.width, self.height)
        if pix_map.width() > self.width or pix_map.height() > self.height:
            pix_map = pix_map.scaled(self.width, self.height, Qt.KeepAspectRatio)
        if pix_map.width() <= self.width:
            self.label.move((self.width - pix_map.width()) / 2, 0)
        self.label.setPixmap(pix_map)

    def open_dialog(self):
        file_path = QFileDialog.getOpenFileName(self, 'Открыть файл')[0]
        if file_path:
            image = Image.open(file_path)
            self.filtering_image = ProcessingImage(image)
            self.reload_image(self.filtering_image)

    def save_dialog(self):
        if self.current_image:
            file_path = QFileDialog.getSaveFileName(
                self, 'Сохранить файл', '.',
                'JPG (*.jpg) ;; PNG (*.png) ;; BMP (*.bmp)')[0]
            if file_path:
                self.current_image.image.save(file_path)

    def return_original_image(self):
        if self.filtering_image:
            self.current_image = None
            self.reload_image(self.filtering_image)

    def process_filter(self, filter_name):
        if self.filtering_image:
            filter_method = getattr(self.filtering_image, filter_name)
            result = filter_method()
            self.current_image = result
            self.reload_image(result)


class ProcessingImage:
    def __init__(self, image):
        self.image = image.copy()
        self.draw = ImageDraw.Draw(self.image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pix = self.image.load()

    def to_qt(self):
        return self.image.convert('RGBA')

    def grey(self):
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
        new_image = ProcessingImage(self.image)
        for i in range(new_image.width):
            for j in range(new_image.height):
                a = new_image.pix[i, j][0]
                b = new_image.pix[i, j][1]
                c = new_image.pix[i, j][2]
                new_image.draw.point((i, j), (255 - a, 255 - b, 255 - c))
        return new_image

    def sepia(self):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
