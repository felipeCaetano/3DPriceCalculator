from PySide6.QtWidgets import (
    QGridLayout, QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTabWidget, QTableWidget, QTableView, QTableWidgetItem,
    QVBoxLayout, QWidget,
)
from PySide6.QtGui import QColor, QFont, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from PySide6 import QtCore

from models.machine import MachineData
from ui.delegates.combodelegate import ComboDelegate
from ui.dialogs.machine_dialog import AddMachineDialog
from ui.stylehelper import (
    badge_color, form_label, make_divider, make_section_label, make_success_banner,
    panel_title, styled_combo, styled_input, STYLE_SHEET,
    C_GREEN, C_TEXT3, C_TEXT4,
)


class SettingsWidget(QWidget):
    """Página de configurações do sistema de precificação 3D."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLE_SHEET)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(0)

        # ── Cabeçalho ──────────────────────────────────────────────────
        self.save_btn = QPushButton("Salvar")
        self.save_btn.setObjectName("PrimaryButton")
        self.reset_btn = QPushButton("Restaurar padrões")
        self.reset_btn.setObjectName("GhostButton")

        root.addLayout(self._build_header())
        root.addSpacing(4)
        root.addWidget(make_divider())
        root.addSpacing(0)

        # ── Abas ───────────────────────────────────────────────────────
        tabs = QTabWidget()
        tabs.setDocumentMode(True)          # sem bordas extras ao redor

        mach_tab = QWidget()
        energy_tab = QWidget(); energy_tab.setStyleSheet("background:transparent;")
        work_tab = QWidget(); work_tab.setStyleSheet("background:transparent;")
        ins_tab = QWidget(); ins_tab.setStyleSheet("background:transparent;")
        params_tab = QWidget(); params_tab.setStyleSheet("background:transparent;")

        self._build_machines_tab(mach_tab)
        self._build_energy_tab(energy_tab)
        self._build_work_tab(work_tab)
        self._build_inputs_tab(ins_tab)
        # self._build_params_tab(params_tab)

        tabs.addTab(mach_tab, "  Máquinas  ")
        tabs.addTab(energy_tab, "  Energia  ")
        tabs.addTab(work_tab, "  Mão de obra  ")
        tabs.addTab(ins_tab, "  Insumos  ")
        tabs.addTab(params_tab, "  Parâmetros  ")

        root.addWidget(tabs)
        root.addStretch()

        self._connect_signals()

    # ──────────────────────────────────────────────────────────────────
    # Cabeçalho
    def _build_header(self) -> QHBoxLayout:
        h = QHBoxLayout()
        h.setContentsMargins(0, 0, 0, 12)

        vbox = QVBoxLayout()
        vbox.setSpacing(2)
        title = QLabel("Configurações")
        title.setObjectName("MenuTitle")
        sub = QLabel("Parâmetros do sistema de precificação")
        sub.setObjectName("MenuSubtitle")
        vbox.addWidget(title)
        vbox.addWidget(sub)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addWidget(self.reset_btn)
        btn_row.addWidget(self.save_btn)

        h.addLayout(vbox)
        h.addStretch()
        h.addLayout(btn_row)
        return h

    def _connect_signals(self):
        self.reset_btn.clicked.connect(self.clear)
        self.save_btn.clicked.connect(self.save)
        self.mach_add_btn.clicked.connect(self.add_machine)
        #self.work_add_btn.clicked.connect(self.add_work_type)

    def clear(self): print("clear forms")
    def save(self): print("salvando configurações")

    def add_machine(self):
        dlg = AddMachineDialog(parent=self)
        dlg.machine_added.connect(self._insert_machine_row)
        dlg.show()

    def _insert_machine_row(self, data: MachineData):
        """Recebe MachineData e atualiza a tabela com uma nova linha."""
        table = self.mach_table
        model = table.model()
        model.rowCount()
    
        row_values = (
            data.model,
            data.brand,
            f"R$ {data.preco:_.2f}".replace("_", "."),
            f"{data.potencia_w} W",
            f"{data.amort_meses} meses",
            f"R$ {data.custo_hora:.2f}",
            ["Ativa","Inativa"],
        )
        self._fill_machine_row(model.rowCount(), row_values)
        self._update_table_footer(model)

    def _update_table_footer(self, model):
        # Atualiza rodapé
        total  = model.rowCount()
        ativas = sum(
            1 for r in range(total)
            if model.item(r, 6) and "ativa" in model.item(r, 6).text().lower()
            and "in" not in model.item(r, 6).text().lower()
        )
        self.table_footer.setText(
            f"{total} máquina{'s' if total != 1 else ''} "
            f"· {ativas} ativa{'s' if ativas != 1 else ''}"
            )

    def _fill_machine_row(self, row: int, values: tuple):
        """Preenche uma linha já existente na mach_table."""
        from ui.stylehelper import badge_color
    
        table = self.mach_table
        model = table.model()
        for col, value in enumerate(values):
            if col == 0:
                model.setItem(row, col, QStandardItem(value))
            elif col == 5:  # R$/hora — verde
                self._set_item(
                    model,
                    row, col, value,
                    Qt.AlignCenter, bold=True, fg=QColor(C_GREEN)
                    )
            elif col == 6:  # Status — badge
                item = QStandardItem(value[0])
                item.setData(value, QtCore.Qt.ItemDataRole.UserRole)
                model.setItem(row, col, item)
            else:
                self._set_item(
                    model, row, col, value, Qt.AlignCenter,
                    fg=QColor(C_TEXT3)
                    )

    def add_work_type(self): print("add work type")

    # Helpers comuns
    @staticmethod
    def _make_table(rows: int, cols: int, headers: list[str]) -> QTableWidget:
        tbl = QTableWidget(rows, cols)
        tbl.setHorizontalHeaderLabels(headers)
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tbl.verticalHeader().setVisible(False)
        tbl.setSelectionBehavior(QTableWidget.SelectRows)
        tbl.setAlternatingRowColors(True)
        tbl.setShowGrid(False)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        return tbl

    @staticmethod
    def _set_item(
        table: QTableWidget | QStandardItemModel,
        row: int, col: int,
        text: str,
        align: Qt.AlignmentFlag = Qt.AlignCenter,
        bold: bool = False,
        fg: QColor | None = None,
        bg: QColor | None = None,
    ):
        item = QStandardItem(text)
        item.setTextAlignment(align)
        if bold:
            f = QFont(); f.setBold(True); item.setFont(f)
        if fg:
            item.setForeground(fg)
        if bg:
            item.setBackground(bg)
        table.setItem(row, col, item)

    @staticmethod
    def _tab_bar_row() -> QHBoxLayout:
        """Barra de descrição + botão add no topo de cada aba."""
        h = QHBoxLayout()
        h.setContentsMargins(0, 8, 0, 8)
        return h

    # Aba: MÁQUINAS
    def _build_machines_tab(self, tab: QWidget):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(8)

        # Barra superior
        top = QHBoxLayout()
        desc = QLabel("Impressoras disponíveis, custos e amortização")
        desc.setObjectName("MenuSubtitle")
        self.mach_add_btn = QPushButton("+ Adicionar máquina")
        self.mach_add_btn.setObjectName("AddBtn")
        top.addWidget(desc)
        top.addStretch()
        top.addWidget(self.mach_add_btn)
        layout.addLayout(top)

        # Tabela
        headers = ["Modelo", "Marca", "Custo", "Potência", "Amortiz.", "R$/hora", "Status"]
        self.mach_table = QTableView()

        self.model = QStandardItemModel(3, 7)
        self.model.setHorizontalHeaderLabels(headers)

        data = [
            ("Ender-3 V3 SE", "Creality", "R$ 899,00", "270 W", "24 meses", "R$ 1,25", ["Ativa", "Inativa"]),
            ("P1S", "Bambu Lab", "R$ 7.490,00", "350 W", "36 meses", "R$ 6,92", ["Ativa", "Inativa"]),
            ("Saturn 4 Ultra","Elegoo", "R$ 3.200,00", "50 W", "30 meses", "R$ 3,56", ["Ativa", "Inativa"]),
        ]

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                if col == 0:   # Modelo — alinhado à esquerda, bold
                    self.model.setItem(row, col, QStandardItem(value))
                elif col == 5:  # R$/hora — verde + bold
                    self._set_item(
                        self.model,
                        row, col, value,
                        Qt.AlignCenter, bold=True, fg=QColor(C_GREEN)
                        )
                elif col == 6:  # Status — badge colorido
                    item = QStandardItem(value[-1])
                    item.setData(value, QtCore.Qt.ItemDataRole.UserRole)
                    self.model.setItem(row, col, item)
                else:
                    self._set_item(
                        self.model, row, col, value, Qt.AlignCenter,
                         fg=QColor(C_TEXT3)
                         )

        self.mach_table.setModel(self.model)

        delegate = ComboDelegate(self.mach_table)
        self.mach_table.setItemDelegateForColumn(6, delegate)

        self.mach_table.setRowHeight(0, 40)
        self.mach_table.setRowHeight(1, 40)
        self.mach_table.setRowHeight(2, 40)
        layout.addWidget(self.mach_table)

        # Rodapé
        self.table_footer = QLabel()
        self.table_footer.setAlignment(Qt.AlignRight)
        self.table_footer.setObjectName("FooterLabel")
        self._update_table_footer(self.model)
        layout.addWidget(self.table_footer)

    # Aba: ENERGIA
    def _build_energy_tab(self, tab: QWidget):
        outer = QHBoxLayout(tab)
        outer.setContentsMargins(0, 8, 0, 8)
        outer.setSpacing(12)

        # ── Card esquerdo: componentes ──────────────────────────────
        left_card = QWidget()
        left_card.setProperty("class", "Card")
        left_layout = QVBoxLayout(left_card)
        left_layout.setSpacing(6)

        left_layout.addWidget(panel_title("Componentes da tarifa"))
        left_layout.addSpacing(4)

        for label_text, default in [
            ("TE — Tarifa de Energia (R$/kWh)", "0,4521"),
            ("TUSD — Uso do sistema (R$/kWh)",  "0,3814"),
        ]:
            row = QHBoxLayout()
            lbl = form_label(label_text)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            inp = styled_input(value=default)
            inp.setFixedWidth(90)
            inp.setAlignment(Qt.AlignRight)
            row.addWidget(lbl)
            row.addWidget(inp)
            left_layout.addLayout(row)

        left_layout.addWidget(make_divider())

        tax_title = form_label("Impostos sobre energia:")
        left_layout.addWidget(tax_title)

        for label_text, default in [
            ("ICMS (%)",   "27,5"),
            ("PIS (%)",    "0,65"),
            ("COFINS (%)", "3,00"),
        ]:
            row = QHBoxLayout()
            lbl = form_label(label_text)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            inp = styled_input(value=default)
            inp.setFixedWidth(90)
            inp.setAlignment(Qt.AlignRight)
            row.addWidget(lbl)
            row.addWidget(inp)
            left_layout.addLayout(row)

        left_layout.addStretch()
        outer.addWidget(left_card, stretch=2)

        # ── Coluna direita ──────────────────────────────────────────
        right = QVBoxLayout()
        right.setSpacing(12)

        # Card bandeira
        flag_card = QWidget()
        flag_card.setProperty("class", "Card")
        flag_layout = QVBoxLayout(flag_card)
        flag_layout.setSpacing(6)
        flag_layout.addWidget(panel_title("Bandeira tarifária"))
        flag_combo = styled_combo([
            "Verde — R$ 0,000 / kWh",
            "Amarela — R$ 0,01874 / kWh",
            "Vermelha Pt. 1 — R$ 0,03971 / kWh",
            "Vermelha Pt. 2 — R$ 0,09492 / kWh",
        ], current=2)
        flag_layout.addWidget(flag_combo)
        disclaimer = QLabel("Atualizada mensalmente pela ANEEL.")
        disclaimer.setObjectName("MenuSubtitle")
        flag_layout.addWidget(disclaimer)

        # Card custo calculado
        calc_card = QWidget()
        calc_card.setProperty("class", "Card")
        calc_card.setStyleSheet(
            "QWidget[class='Card'] { background-color: #f0fdf4; border: 1px solid #bbf7d0; }"
        )
        calc_layout = QVBoxLayout(calc_card)
        calc_layout.setSpacing(4)

        calc_title = QLabel("Custo efetivo calculado")
        calc_title.setObjectName("SectionLabel")
        calc_title.setStyleSheet("color: #15803d; background: transparent;")

        calc_value = QLabel(f"R$ {self._calculate_energy_cost()} / kWh")
        calc_value.setObjectName("HighlightValue")

        calc_detail = QLabel(
            "TE + Bandeira:  R$ 0,4918\n"
            "TUSD:            R$ 0,3814\n"
            "Impostos:        R$ 0,1994"
        )
        calc_detail.setObjectName("MenuSubtitle")

        calc_layout.addWidget(calc_title)
        calc_layout.addWidget(calc_value)
        calc_layout.addSpacing(4)
        calc_layout.addWidget(calc_detail)

        right.addWidget(flag_card)
        right.addWidget(calc_card)
        right.addStretch()

        outer.addLayout(right, stretch=1)

    def _calculate_energy_cost(self) -> str:
        return "1,0726"

    # Aba: MÃO DE OBRA
    def _build_work_tab(self, tab: QWidget):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(8)

        # Barra superior
        top = QHBoxLayout()
        desc = QLabel("Tipos de mão de obra e encargos trabalhistas")
        desc.setObjectName("MenuSubtitle")
        self.work_add_btn = QPushButton("+ Adicionar")
        self.work_add_btn.setObjectName("AddBtn")
        top.addWidget(desc)
        top.addStretch()
        top.addWidget(self.work_add_btn)
        layout.addLayout(top)

        # Tabela
        headers = ["Função", "R$/hora", "Encargos", "Custo total/h"]
        table = QTableView()

        model = QStandardItemModel(3, 4)
        model.setHorizontalHeaderLabels(headers)

        data = [
            ("Operador/Monitoramento", "R$ 18,00", "67,8%", "R$ 30,20"),
            ("Pós-Processamento",        "R$ 22,00", "67,8%", "R$ 36,91"),
            ("Design/Modelagem 3D",    "R$ 60,00", "—",     "R$ 60,00"),
        ]

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                if col == 0:
                    self._set_item(
                        model, row, col, value, Qt.AlignVCenter | Qt.AlignLeft
                        )
                elif col == 3:
                    self._set_item(
                        model,
                        row, 
                        col, 
                        value, 
                        Qt.AlignCenter, 
                        bold=True, 
                        fg=QColor(C_GREEN)
                        )
                else:
                    self._set_item(
                        model,
                        row, 
                        col, 
                        value, 
                        Qt.AlignCenter, 
                        fg=QColor(C_TEXT3)
                        )
        
        table.setModel(model)
        table.setRowHeight(0, 40)
        table.setColumnWidth(0, 200)
        table.setRowHeight(1, 40)
        table.setRowHeight(2, 40)
        layout.addWidget(table)

        # Card encargos
        enc_card = QWidget()
        enc_card.setProperty("class", "Card")
        enc_layout = QVBoxLayout(enc_card)
        enc_layout.setSpacing(8)

        enc_layout.addWidget(panel_title("Encargos trabalhistas aplicados"))

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(4)

        charges = [
            ("INSS patronal (%)", "20,00"),
            ("FGTS (%)", "8,00"),
            ("13º + Férias (%)", "26,70"),
            ("Outros (%)", "13,10"),
        ]
        for col, (lbl_text, default) in enumerate(charges):
            grid.addWidget(form_label(lbl_text), 0, col)
            inp = styled_input(value=default)
            inp.setAlignment(Qt.AlignRight)
            grid.addWidget(inp, 1, col)

        enc_layout.addLayout(grid)
        enc_layout.addWidget(
            make_section_label(f"Total encargos: {self._calculate_work()}% sobre o salário-hora")
        )
        layout.addWidget(enc_card)

    def _calculate_work(self) -> str:
        return "67,8"

    # Aba: INSUMOS
    def _build_inputs_tab(self, tab: QWidget):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(8)

        top = QHBoxLayout()
        desc = QLabel("Filamentos, resinas e consumíveis com preço, densidade e perda")
        desc.setObjectName("MenuSubtitle")
        add_btn = QPushButton("+ Adicionar material")
        add_btn.setObjectName("AddBtn")
        top.addWidget(desc)
        top.addStretch()
        top.addWidget(add_btn)
        layout.addLayout(top)

        headers = ["Material", "Marca", "R$/kg", "g/cm³", "R$/cm³", "Perda %", "Temp.", "Tipo"]
        table = QTableView()
        model = QStandardItemModel(5, 8)
        model.setHorizontalHeaderLabels(headers)

        data = [
            ("PLA+", "Polymaker", "R$ 89,90",  "1,24", "R$ 0,111", "5%",  "215 °C", "FDM"),
            ("PETG", "eSUN",      "R$ 94,00",  "1,27", "R$ 0,119", "6%",  "235 °C", "FDM"),
            ("ABS",     "Bambu Lab", "R$ 120,00", "1,04", "R$ 0,125", "8%",  "245 °C", "FDM"),
            ("TPU 95A", "Polymaker", "R$ 189,00", "1,21", "R$ 0,229", "4%",  "230 °C", "FDM"),
            ("ABS-Like","Elegoo",    "R$ 189,00", "1,11", "R$ 0,210", "4%",  "—",      "Resina"),
        ]

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                if col == 0:
                    self._set_item(model, row, col, value, Qt.AlignVCenter | Qt.AlignLeft, bold=True)
                elif col == 4:   # R$/cm³ — verde
                    self._set_item(model, row, col, value, Qt.AlignCenter, fg=QColor(C_GREEN))
                elif col == 5:   # Perda % — laranja
                    self._set_item(model, row, col, value, Qt.AlignCenter, fg=QColor("#d97706"))
                else:
                    self._set_item(model, row, col, value, Qt.AlignCenter, fg=QColor(C_TEXT3))
        
        table.setModel(model)

        for r in range(5):
            table.setRowHeight(r, 38)
        layout.addWidget(table)

    # Aba: PARÂMETROS GERAIS
    def _build_params_tab(self, tab: QWidget):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(10)

        # Linha 1
        row1 = QHBoxLayout()
        row1.setSpacing(12)
        row1.addWidget(self._build_overhead_card(), stretch=1)
        row1.addWidget(self._build_markup_card(), stretch=1)
        layout.addLayout(row1)

        # Linha 2
        row2 = QHBoxLayout()
        row2.setSpacing(12)
        row2.addWidget(self._build_print_params_card(), stretch=1)
        row2.addWidget(self._build_maintenance_card(), stretch=1)
        layout.addLayout(row2)

    def _build_overhead_card(self) -> QWidget:
        card = QWidget(); card.setProperty("class", "Card")
        cl = QVBoxLayout(card); cl.setSpacing(6)
        cl.addWidget(panel_title("Custos fixos & overhead"))

        for lbl_text, default, hint in [
            ("Custo fixo mensal total (R$)", "1.500,00", "Aluguel, internet, limpeza…"),
            ("Horas produtivas por mês",     "480",      None),
        ]:
            cl.addWidget(form_label(lbl_text))
            inp = styled_input(value=default)
            cl.addWidget(inp)
            if hint:
                h = QLabel(hint); h.setObjectName("FooterLabel"); cl.addWidget(h)

        cl.addStretch()
        cl.addWidget(make_section_label("Overhead por hora: R$ 3,13"))
        return card

    def _build_markup_card(self) -> QWidget:
        card = QWidget(); card.setProperty("class", "Card")
        cl = QVBoxLayout(card); cl.setSpacing(6)
        cl.addWidget(panel_title("Markup & tributação"))

        for lbl_text, default in [
            ("Markup padrão sobre custo (%)", "150"),
            ("ISS — Imposto sobre serviços (%)", "5,00"),
            ("Simples Nacional (%)", "6,00"),
        ]:
            row = QHBoxLayout()
            lbl = form_label(lbl_text)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            inp = styled_input(value=default)
            inp.setFixedWidth(90); inp.setAlignment(Qt.AlignRight)
            row.addWidget(lbl); row.addWidget(inp)
            cl.addLayout(row)

        cl.addStretch()
        cl.addWidget(make_section_label("Carga tributária total estimada: 11,0%"))
        return card

    def _build_print_params_card(self) -> QWidget:
        card = QWidget(); card.setProperty("class", "Card")
        cl = QVBoxLayout(card); cl.setSpacing(6)
        cl.addWidget(panel_title("Parâmetros de impressão"))

        for lbl_text, default in [
            ("Taxa de falha estimada (%)",    "4,0"),
            ("Tempo de setup por job (min)",  "15"),
            ("Desperdício de material (%)",   "3,0"),
            ("Custo de frete médio (R$)",     "22,00"),
        ]:
            row = QHBoxLayout()
            lbl = form_label(lbl_text)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            inp = styled_input(value=default)
            inp.setFixedWidth(90); inp.setAlignment(Qt.AlignRight)
            row.addWidget(lbl); row.addWidget(inp)
            cl.addLayout(row)

        cl.addStretch()
        return card

    def _build_maintenance_card(self) -> QWidget:
        card = QWidget(); card.setProperty("class", "Card")
        cl = QVBoxLayout(card); cl.setSpacing(6)
        cl.addWidget(panel_title("Manutenção & peças de reposição"))

        for lbl_text, default in [
            ("Custo mensal manutenção (R$)", "80,00"),
            ("Vida útil do bico (horas)", "500"),
            ("Custo por bico (R$)", "18,00"),
            ("Troca de cama (meses)", "6"),
        ]:
            row = QHBoxLayout()
            lbl = form_label(lbl_text)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            inp = styled_input(value=default)
            inp.setFixedWidth(90); inp.setAlignment(Qt.AlignRight)
            row.addWidget(lbl); row.addWidget(inp)
            cl.addLayout(row)

        cl.addStretch()
        return card
