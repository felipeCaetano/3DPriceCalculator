from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.stylehelper import form_label, make_divider, styled_combo, \
    styled_input, STYLE_SHEET


class SettingsWidget(QWidget):
    """Página que mostra todas as configurações disponíveis como impressora
    e energia elétrica"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Configurações")
        title.setObjectName("MenuTitle")

        layout.addWidget(title)
        layout.addWidget(make_divider())

        layout.addStretch()