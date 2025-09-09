# 原来的 import
# from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QDesktopWidget
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt

# 改成 PySide6
from PySide6.QtWidgets import QLabel, QApplication, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication

import sys
import os



class FloatingPet(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)

        # 加载并缩放图片
        BASE_DIR = os.path.dirname(__file__)
        img_path = lambda name: os.path.join(BASE_DIR, "images", name)

        self.normal_img = QPixmap(img_path("normal.png")).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.remind_img = QPixmap(img_path("remind.png")).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.study_img = QPixmap(img_path("study.png")).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label.setPixmap(self.normal_img)
        self.resize(self.normal_img.width(), self.normal_img.height())

        # 屏幕右下角
        screen = QGuiApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 50, screen.height() - self.height() - 100)

    def show_normal(self):
        self.label.setPixmap(self.normal_img)

    def show_reminder(self):
        self.label.setPixmap(self.remind_img)

    def show_study(self):
        self.label.setPixmap(self.study_img)

    # ✅ 拖动支持
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
