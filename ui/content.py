from PySide6.QtCore import Qt, QPropertyAnimation, QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QMdiSubWindow, QWidget, QHBoxLayout, QPushButton, \
    QStyleOption, QStyle, QLabel

from ui.hamburgerbutton import HamburgerButton


class WidgetContent(QWidget):
    def __init__(self, mdi):
        super(WidgetContent, self).__init__()
        self.mdi = mdi
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # self.menu_btn = QPushButton("Menu")
        self.menu_btn = HamburgerButton(self)
        self.menu_btn.move(8, 8)  # canto superior esquerdo

        self.menu_btn.clicked.connect(self.show_menu)
        #self.layout.addWidget(self.menu_btn)
        # self.piece_name_lbl = QLabel(f'Nova Peça - precificação')
        # self.cancel_btn = QPushButton('Cancelar')
        # self.save_btn = QPushButton('Salvar')
        # self.layout.addWidget(self.piece_name_lbl)
        # self.layout.addWidget(self.cancel_btn)
        # self.layout.addWidget(self.save_btn)
        self.menu_btn.raise_()

    def show_menu(self):
        self.animation = QPropertyAnimation(self.mdi.menu, b"size")
        self.animation.setDuration(150)
        if self.menu_btn.isChecked():
            self.animation.setStartValue(QSize(0, self.mdi.height()))
            self.animation.setEndValue(QSize(270, self.mdi.height()))
        else:
            # fechando
            self.animation.setStartValue(QSize(270, self.mdi.height()))
            self.animation.setEndValue(QSize(0, self.mdi.height()))

        self.animation.valueChanged.connect(self._move_btn)
        self.animation.start()
        if self.menu_btn.isChecked():
            self.mdi.overlay.show()
            self.mdi.menu.show()
            self.mdi.setActiveSubWindow(self.mdi.overlay)
            self.mdi.setActiveSubWindow(self.mdi.menu)
        else:
            self.animation.finished.connect(self._close_menu)

    def _move_btn(self, value):
        self.menu_btn.move(value.width() + 8, 8)  # canto superior esquerdo
        self.menu_btn.raise_()

    def _close_menu(self):
        self.mdi.overlay.hide()
        self.mdi.menu.hide()
        self.menu_btn.move(8, 8)
        self.menu_btn.raise_()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

class Content(QMdiSubWindow):
    def __init__(self, parent):
        super(Content, self).__init__()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.widget = WidgetContent(parent)
        self.setWidget(self.widget)