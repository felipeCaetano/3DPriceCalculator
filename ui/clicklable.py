from PySide6.QtCore import Signal, Qt, Slot
from PySide6.QtWidgets import QLabel, QFrame, QColorDialog


class ClickableLabel(QLabel):
    # Define a custom signal
    clicked = Signal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Frame clicked!")
            self.clicked.emit()
            # Always call the parent implementation to ensure standard behavior
        super().mousePressEvent(event)


class ColoredDot(QFrame):
    # Optional: Create a custom signal to use it like a QPushButton
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
        # Always call the parent implementation to ensure standard behavior
        super().mousePressEvent(event)

    @Slot(str)
    def handle_data(self, data):
        self.setStyleSheet(f"background:{data};"
                           f" border-radius:9px; "
                           f"border:0.5px solid #D3D1C7;")
