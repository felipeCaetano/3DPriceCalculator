from functools import partial

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QVBoxLayout, QLabel,
                               QPushButton, QFrame, QGraphicsDropShadowEffect)

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
        title = QLabel("Print3D Manager", objectName="AppTitle")
        subtitle = QLabel("Controle de produção", objectName="MenuSubtitle")
        
        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(subtitle)

        # Menu Items
        labels = [
            ("PRINCIPAL", False, None, None, None),
            ("Dashboard", True,  "res/img/icons/dashboard.png", parent._navigate, 0),
            ("Nova peça", False,  "res/img/icons/3dpiece.png", None, None),
            ("Histórico", False, "res/img/icons/history.png", None, None),
            ("Divider", False, None, None, None),
            ("ESTOQUE", False, None, None, None),
            ("Filamentos", False, "res/img/icons/filament.png", parent._navigate, 1),
            ("Relatórios", False, "res/img/icons/report.png", None, None),
            ("Divider", False, None, None, None),
            ("Configurações", False, "res/img/icons/settings.png", parent._navigate, 2)
        ]

        for text, is_active, icon_path, callback, index in labels:
            if text in ["PRINCIPAL", "ESTOQUE"]:
                lbl = QLabel(text, objectName="SectionLabel")
                # lbl.setStyleSheet(
                #     "color: #888780;"
                #     "font-size: 10px;"
                #     " letter-spacing: 1px; font-weight: bold; margin-top: 2px;"
                # )
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
                    btn.clicked.connect(partial(callback, index))
                btn.setCursor(Qt.PointingHandCursor)
                sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch() 

