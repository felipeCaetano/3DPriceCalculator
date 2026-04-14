import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMdiArea

from ui.content import Content
from ui.overlay import Overlay
from ui.sidemenu import SideMenu


class MdiArea(QMdiArea):
    def __init__(self):
        super(MdiArea, self).__init__()
        self.menu = SideMenu()
        self.content= Content(self) 
        self.overlay = Overlay(self)

        self.addSubWindow(self.content)
        self.addSubWindow(self.overlay)
        self.addSubWindow(self.menu)

    def resizeEvent(self, event):
        self.content.resize(self.width(), self.height())
        self.overlay.resize(self.width(), self.height())
        self.menu.resize(270, self.height())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora 3D")
        self.mdi = MdiArea()
        self.setCentralWidget(self.mdi)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
