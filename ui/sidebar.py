from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
 QPushButton, QFrame, QLineEdit,  QGridLayout,  QGraphicsDropShadowEffect)
from PySide6.QtGui import QFont, QIcon, QColor
from PySide6.QtCore import Qt, QSize

from ui.stylehelper import make_divider


class Sidebar(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setContentsMargins(8, 8, 8, 8)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        self.setGraphicsEffect(shadow)

        # Header Sidebar
        title = QLabel("Print3D Manager")
        title.setObjectName("MenuTitle")
        subtitle = QLabel("Controle de produção")
        subtitle.setObjectName("MenuSubtitle")
        
        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(subtitle)

        # Menu Items
        labels = [
            ("PRINCIPAL", False, None, None),
            ("Dashboard", True,  "res/img/icons/dashboard.png", None),
            ("Nova peça", False,  "res/img/icons/3dpiece.png", None),
            ("Histórico", False, "res/img/icons/history.png", None),
            ("Divider", False, None, None),
            ("ESTOQUE", False, None, None),
            ("Filamentos", False, "res/img/icons/filament.png", parent._filament_manager),
            ("Relatórios", False, "res/img/icons/report.png", None),
            ("Divider", False, None, None),
            ("Configurações", False, "res/img/icons/settings.png", None)
        ]

        for text, is_active, icon_path, callback in labels:
            if text in ["PRINCIPAL", "ESTOQUE"]:
                lbl = QLabel(text)
                lbl.setStyleSheet(
                    "color: #888780;"
                    "font-size: 10px;"
                    " letter-spacing: 1px; font-weight: bold; margin-top: 2px;"
                )
                sidebar_layout.addWidget(lbl)
            elif text == "Divider":
                sidebar_layout.addWidget(make_divider())
            else:
                btn = QPushButton(f"{text}")
                btn.setObjectName("MenuButton")
                btn.setProperty("active", str(is_active).lower())
                icon = QIcon(icon_path)
                btn.setIcon(icon)
                btn.setIconSize(QSize(18, 18))
                if callback:
                    btn.clicked.connect(callback)
                btn.setCursor(Qt.PointingHandCursor)
                sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

