# coding=utf-8
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTabWidget, QWidget, QTabBar


class Pagina(QTabWidget):

    def __init__(self, *args, **kwargs):
        super().__init__()

    def resizeEvent(self, event):
        self.tabBar().setMinimumWidth(self.width())
        super().resizeEvent(event)

class TabPagina(QTabBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tabSizeHint(self, index):
        size = super().tabSizeHint(index)
        offset = self.width()
        for index in range(self.count()):
            offset -= super().tabSizeHint(index).width()
        size.setWidth(max(size.width(), size.width() + offset))
        return size