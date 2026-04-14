from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMdiSubWindow


class Overlay(QMdiSubWindow):
    def __init__(self, parent):
        super(Overlay, self).__init__()
        self.parent = parent
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setStyleSheet("background: rgba(0, 0, 0, 15%);")
        self.hide()

    def mousePressEvent(self, event):
        content_widget = self.parent.content.widget
        content_widget.menu_btn.setChecked(False)
        content_widget.show_menu()

    def animation_end(self):
        self.parent.menu.hide()