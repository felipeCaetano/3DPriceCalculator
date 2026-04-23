import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QStackedWidget,
                               QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QLineEdit, QComboBox,
                               QProgressBar, QTextEdit, QGridLayout,
                               QGraphicsDropShadowEffect, QScrollArea)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QColor

from ui.stylehelper import make_divider, styled_combo, STYLE_SHEET
from ui.clicklable import ClickableLabel, ColoredDot
from ui.filament import FilamentCard, FilamentForm, FilamentPageWidget
from ui.dashboard import DashBoard
from ui.sidebar import Sidebar      
                 

class Print3DManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Print3D Manager")
        self.resize(1100, 800)
        self.setStyleSheet(STYLE_SHEET)
 
        self.stack = QStackedWidget()

        # Layout Principal (HBox: Sidebar + Main Content)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)
        self.tela_dashboard = DashBoard()
        self.tela_filamentos = FilamentPageWidget()
        self.stack.addWidget(self.tela_dashboard)
        self.stack.addWidget(self.tela_filamentos)
        main_layout.addWidget(self.stack)

    def _filament_manager(self, index):
        self.stack.setCurrentIndex(1)

   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Print3DManager()
    window.show()
    sys.exit(app.exec())
