from PySide6.QtWidgets import QHBoxLayout, QHeaderView, QLabel, QPushButton, \
 QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QSize

from ui.stylehelper import form_label, make_divider, styled_combo, \
    styled_input, STYLE_SHEET


class SettingsWidget(QWidget):
    """Página que mostra todas as configurações disponíveis
    como impressora e energia elétrica"""

    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLE_SHEET)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.save_btn = QPushButton("Salvar")
        self.save_btn.setObjectName("PrimaryButton")
        self.reset_btn = QPushButton("Restaurar Padrões")
        self.reset_btn.setObjectName("PrimaryButton")
        top_layout = self._create_header()
        layout.addLayout(top_layout)
        layout.addWidget(make_divider())
        tabs = QTabWidget()
        machines_tab = QWidget()
        self.setup_machines_tab(machines_tab)
        
        tabs.addTab(machines_tab, "Máquinas")
        tabs.addTab(QWidget(), "Energia")
        tabs.addTab(QWidget(), "Mão de obra")
        tabs.addTab(QWidget(), "Insumos")
        tabs.addTab(QWidget(), "Parâmetros")

        layout.addWidget(tabs)
        layout.addStretch()
        self._connect_signals()
    
    def _create_header(self):
        layout_H = QHBoxLayout()
        layout_V = QVBoxLayout()
        title = QLabel("Configurações")
        title.setObjectName("MenuTitle")
        subtitle = QLabel("Parâmetros do sistema de precificação")
        subtitle.setObjectName("MenuSubtitle")
        layout_V.addWidget(title)
        layout_V.addWidget(subtitle)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.save_btn)
        layout_H.addLayout(layout_V)
        layout_H.addStretch()
        layout_H.addLayout(btn_layout)
        return layout_H
    
    def _connect_signals(self):
        self.reset_btn.clicked.connect(self.clear)
        self.save_btn.clicked.connect(self.save)
        self.add_btn.clicked.connect(self.add_machine)

    def add_machine(self):
        print("add machine")
    
    def clear(self):
        print("clear forms")

    def save(self):
        print("salvando as tabelas")
    

    def setup_machines_tab(self, tab):
        layout = QVBoxLayout(tab)
        top_bar = QHBoxLayout()
        desc = QLabel("Impressoras disponíveis, custos e amortização")
        desc.setStyleSheet("color: #666;")
        self.add_btn = QPushButton("+ Adicionar máquina")
        self.add_btn.setObjectName("AddBtn")
        top_bar.addWidget(desc)
        top_bar.addStretch()
        top_bar.addWidget(self.add_btn)
        layout.addLayout(top_bar)
        table = QTableWidget(3, 7)
        table.setHorizontalHeaderLabels(
            [
                "Modelo",
                "Marca",
                "Custo",
                "Potência",
                "Amortiz.",
                "R$/hora",
                "Status"
            ]
        )
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        
        data = [
            ["Ender-3 V3 SE", "Creality", "R$ 899,00", "270 W", "24 meses",
             "R$ 1,25", "Ativa"],
            ["P1S", "Bambu Lab", "R$ 7.490,00", "350 W", "36 meses",
            "R$ 6,92", "Ativa"],
            ["Saturn 4 Ultra", "Elegoo", "R$ 3.200,00", "50 W", "30 meses",
            "R$ 3,56", "Inativa"],
        ]

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 5: # R$/hora
                    item.setForeground(Qt.darkGreen)
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                table.setItem(row, col, item)

        layout.addWidget(table)
        
        footer = QLabel("3 máquinas · 2 ativas")
        footer.setAlignment(Qt.AlignRight)
        footer.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(footer)
