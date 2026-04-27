from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QColorDialog, QFrame, QLabel


class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            # Always call the parent implementation to ensure standard behavior
        super().mousePressEvent(event)


class ColoredDot(QFrame):
    clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(2)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            color = QColorDialog.getColor()
            if color.isValid():
                self.clicked.emit(color.name())
        super().mousePressEvent(event)

    @Slot(str)
    def handle_data(self, data):
        self.setStyleSheet(f"background:{data};"
                           f"border-radius: 9px;"
                           f"border:0.5px solid #D3D1C7;")
