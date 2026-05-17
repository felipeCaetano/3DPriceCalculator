import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QStackedWidget,
                               QWidget, QHBoxLayout)

from ui.dashboard import DashBoard
from ui.filament import FilamentPageWidget
from ui.settings import SettingsWidget
from ui.sidebar import Sidebar
from ui.stylehelper import STYLE_SHEET


class Print3DManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Print3D Manager")
        self.resize(1100, 800)
        self.setStyleSheet(STYLE_SHEET)
 
        self.stack = QStackedWidget()
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
        self.tela_config = SettingsWidget()
        self.stack.addWidget(self.tela_dashboard)
        self.stack.addWidget(self.tela_filamentos)
        self.stack.addWidget(self.tela_config)
        main_layout.addWidget(self.stack)

    def _navigate(self, value):
        self.stack.setCurrentIndex(value)

   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    window = Print3DManager()
    window.show()
    sys.exit(app.exec())
