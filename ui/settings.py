from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QHeaderView, QLabel, QPushButton, \
 QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QSize

from ui.stylehelper import form_label, make_divider, make_section_label, panel_title, styled_combo, \
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
        energy_tab = QWidget()
        work_tab = QWidget()
        self.setup_machines_tab(machines_tab)
        self.setup_energy_tab(energy_tab)
        self.setup_work_tab(work_tab)
        
        tabs.addTab(machines_tab, "Máquinas")
        tabs.addTab(energy_tab, "Energia")
        tabs.addTab(work_tab, "Mão de obra")
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

    def setup_energy_tab(self, tab):
        layout = QHBoxLayout(tab)
        content = QWidget()
        content_layout = QVBoxLayout()
        content.setProperty("class", "Card")
        content_title = QLabel("Componentes da Tarifa")
        content_title.setObjectName("MenuSubtitle")
        content_layout.addWidget(content_title)
        row1 = QHBoxLayout()
        row1.addWidget(form_label("TE — Tarifa de Energia\n(R$/kWh)"))
        te_input = styled_input("0,4521")
        row1.addWidget(te_input)
        content_layout.addLayout(row1)
        row2 = QHBoxLayout()
        row2.addWidget(form_label("TUSD — Uso do sistema\n(R$/kWh)"))
        tusd_input = styled_input("0,3814")
        row2.addWidget(tusd_input)
        content_layout.addLayout(row2)
        content_layout.addWidget(make_divider())
        content_tax = QLabel("Impostos sobre energia")
        content_tax.setObjectName("MenuSubtitle")
        content_layout.addWidget(content_tax)
        row3 = QHBoxLayout()
        row3.addWidget(form_label("ICMS (%)"))
        icms_input = styled_input("27,5")
        row3.addWidget(icms_input)
        content_layout.addLayout(row3)
        row4 = QHBoxLayout()
        row4.addWidget(form_label("PIS (%)"))
        pis_input = styled_input("0,65")
        row4.addWidget(pis_input)
        content_layout.addLayout(row4)
        row5 = QHBoxLayout()
        row5.addWidget(form_label("COFINS (%)"))
        cofins_input = styled_input("3")
        row5.addWidget(cofins_input)
        content_layout.addLayout(row5)
        content.setLayout(content_layout)
        layout.addWidget(content)

        flag = QWidget()
        flag.setProperty("class", "Card")
        flag_layout = QVBoxLayout()
        flag_title = QLabel("Bandeira Tarifária:")
        flag_title.setObjectName("MenuSubtitle")
        flag_layout.addWidget(flag_title)
        flag.setLayout(flag_layout)
        flag_input = styled_combo(
            ["Verde", "Amarela", "Vermelha pt. 1", "Vermelha pt. 2"]
        )
        flag_layout.addWidget(flag_input)
        flag_disclaimer = QLabel("Atualizada mensalmente pela ANEEL.")
        flag_disclaimer.setObjectName("MenuSubtitle")

        energy_cost = QWidget()
        energy_cost.setProperty("class", "Card")
        energy_cost_layout = QVBoxLayout()
        energy_cost_title = QLabel("Custo efetivo calculado")
        energy_cost_value = QLabel(f"R$ {self._calculate_value()}/kWh")
        energy_cost_layout.addWidget(energy_cost_title)
        energy_cost_layout.addWidget(energy_cost_value)
        energy_cost_te = QLabel("TE + Bandeira: ")
        energy_cost_te.setObjectName("MenuSubtitle")
        energy_cost_layout.addWidget(energy_cost_te)
        energy_cost.setLayout(energy_cost_layout)

        right_layout = QVBoxLayout()
        layout.addLayout(right_layout)
        right_layout.addWidget(flag)
        right_layout.addWidget(energy_cost)

        layout.addStretch()

    def _calculate_value(self):
        return "1,07"
    
    def setup_work_tab(self, tab):
        layout = QVBoxLayout(tab)
        top_bar = QHBoxLayout()
        desc = QLabel("Tipos de Mão de Obra")
        desc.setStyleSheet("color: #666;")
        self.add_btn = QPushButton("+ Adiciona")
        self.add_btn.setObjectName("AddBtn")
        top_bar.addWidget(desc)
        top_bar.addStretch()
        top_bar.addWidget(self.add_btn)
        layout.addLayout(top_bar)
        table = QTableWidget(3, 4)
        table.setHorizontalHeaderLabels(
            [
                "Função",
                "R$/h",
                "Encargos",
                "Custo total/h",
            ]
        )
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        
        data = [
            ["Operador / Monitoramento", "R$ 18,00", "67,8%", "R$ 30,20"],
            ["Pós-Processamento", "R$ 22,00", "67,8%", "R$ 36,91"],
            ["Design / Modelagem 3D", "R$ 60,00", "—", "R$ 60,0"],
        ]

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 3: # R$/hora
                    item.setForeground(Qt.darkGreen)
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                table.setItem(row, col, item)

        layout.addWidget(table)
        
        footer = QWidget()
        footer.setProperty("class", "Card")
        footer_layout = QVBoxLayout()
        footer.setLayout(footer_layout)
        footer_layout.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #888; font-size: 14px;")
        footer_title = panel_title("Encargos Trabalhistas Aplicados:")
        footer_layout.addWidget(footer_title)
        footer_grid_layout = QGridLayout()
        footer_grid_layout.setHorizontalSpacing(16)
        footer_grid_layout.setVerticalSpacing(2)
        footer_grid_layout.addWidget(form_label("INSS Patronal (%)"), 0, 0)
        footer_grid_layout.addWidget(styled_input("20.00"), 1, 0)
        footer_grid_layout.addWidget(form_label("FGTS (%)"), 0, 1)
        footer_grid_layout.addWidget(styled_input("8.00"), 1, 1)
        footer_grid_layout.addWidget(form_label("13º + Férias (%)"), 0, 2)
        footer_grid_layout.addWidget(styled_input("26.70"), 1, 2)
        footer_grid_layout.addWidget(form_label("Outros (%)"), 0, 3)
        footer_grid_layout.addWidget(styled_input("13.00"), 1, 3)
        footer_layout.addLayout(footer_grid_layout)
        footer_footer = make_section_label(f"Total encargos: {self._calculate_work()}% sobre o salário-hora")
        footer_layout.addWidget(footer_footer)
        layout.addWidget(footer)

    def _calculate_work(self):
        return "67,8"