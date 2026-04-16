from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QPushButton


class HamburgerButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(36, 36)
        self.setCheckable(True)  # alterna entre aberto/fechado
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("border: none; background: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#185FA5"), 2, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)

        cx, cy = self.width() // 2, self.height() // 2

        if self.isChecked():
            # desenha X quando sidebar está aberta
            painter.drawLine(cx - 7, cy - 7, cx + 7, cy + 7)
            painter.drawLine(cx + 7, cy - 7, cx - 7, cy + 7)
        else:
            # desenha hambúrguer
            for dy in [-5, 0, 5]:
                painter.drawLine(cx - 8, cy + dy, cx + 8, cy + dy)