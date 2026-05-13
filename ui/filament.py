from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (QDateEdit,
    QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QProgressBar, QPushButton, QScrollArea, QSpinBox, QStyle,
    QStyleOption,
    QVBoxLayout, QWidget
)

from models.filament import FilamentData
from ui.clicklable import ColoredDot
from ui.styledmessagebox import StyledMessageBox
from ui.stylehelper import form_label, make_divider, styled_combo, \
    styled_input, STYLE_SHEET


from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from models.filament import FilamentData
from ui.clicklable import ColoredDot
from ui.stylehelper import form_label


class FilamentCard(QFrame):
    """Card de visualização de um FilamentData."""

    edit_requested = Signal(object)
    delete_requested = Signal()

    def __init__(self, filamento: FilamentData):
        super().__init__()
        self.filament = filamento
        self.setProperty("class", "Card")
        self.setFixedHeight(128)
        self.name_lbl = QLabel("Filamento", objectName="PanelTitle")
        self.filament_type = QLabel("PLA")
        self.filament_acabamento = QLabel("Hyper Speed")
        self.filament_brand = QLabel("Anycubic")
        self.filament_price = QLabel("R$ 89,90")
        self.filament_color = ColoredDot()
        self.filament_color.handle_data("#2563EB")
        self.filament_color.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.filament_color.setFixedSize(40, 40)
        self.filament_data_validade = QLabel("12/12/2036")
        self.progress_bar = QProgressBar()
        self.progress_bar.valueChanged.connect(self._update_progressbar_text_color)
        self._setup_layout()
        self._setup_progressbar()

        if filamento:
            self.refresh()

    def _setup_layout(self):
        """Monta a estrutura de layouts do card."""
        root = QHBoxLayout(self)
        root.setContentsMargins(4, 4, 4, 4)
        root.setSpacing(2)
        root.addWidget(self.filament_color, alignment=Qt.AlignVCenter)
        right = QVBoxLayout()
        right.setSpacing(2)
        right.addWidget(self.name_lbl)
        right.addLayout(self._build_grid())
        right.addWidget(form_label("Bobina restante:"))
        right.addWidget(self.progress_bar)
        root.addLayout(right)

    def _build_grid(self):
        """Monta o grid com tipo, marca e preço."""
        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(2)
        grid.addWidget(form_label("Tipo"), 0, 0)
        grid.addWidget(self.filament_type, 1, 0)
        grid.addWidget(form_label("Acabamento"), 0, 1)
        grid.addWidget(self.filament_acabamento, 1, 1)
        grid.addWidget(form_label("Marca"), 0, 2)
        grid.addWidget(self.filament_brand, 1, 2)
        grid.addWidget(form_label("Válido até:"), 0, 3)
        grid.addWidget(self.filament_data_validade, 1, 3)
        grid.addWidget(form_label("Preço/kg"), 0, 4)
        grid.addWidget(self.filament_price, 1, 4)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 1)
        return grid

    def _setup_progressbar(self):
        """Configura aparência da barra de progresso."""
        self._chunk_color = "#2563EB"  # cor padrão, pode mudar depois
        self.progress_bar.setValue(64)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(14)

    def _update_progressbar_text_color(self, value: int):
        """Troca a cor do texto para contraste com o chunk."""
        text_color = "white" if value > 50 else "#2C2C2A"
        if self._chunk_color == "#ffffff":
            text_color = "black"
        elif self._chunk_color == "#000000":
            text_color = "white"
        
        self.progress_bar.setStyleSheet(
            f" color: {text_color};"
            f" background: {self._chunk_color};"  
        )

    def refresh(self):
        """Atualiza os labels com os dados atuais do modelo."""
        self._chunk_color = self.filament.cor_str
        self.name_lbl.setText(
            f"{self.filament.marca} {self.filament.tipo}"
            f" — {self.filament.cor.upper()}"
        )
        self.filament_type.setText(self.filament.tipo)
        self.filament_brand.setText(self.filament.marca)
        self.filament_price.setText(
            f"R$ {self.filament.preco_kg:.2f}".replace(".", ",")
        )
        self.filament_color.handle_data(self.filament.cor_str or "#888780")
        value = self.filament.bobina_restante_pct
        self.data_validade.setDate(QDate.currentDate())
        self.progress_bar.setValue(value)
        self._update_progressbar_text_color(value)    


class FilamentForm(QWidget):
    """Formulário lateral para criar ou editar um FilamentData."""
    saved = Signal(object)  # emite o FilamentData salvo
    cancelled = Signal()

    TIPOS = [
        "PLA", "PETG", "ABS", "TPU", "ASA", "Nylon", "HIPS"
    ]
    ACABAMENTOS = [
        "Hyper Speed", "Matte", "Silk", "Metalizado", "Sólido",
        "Condutivo", "Premium", "Velvet"
    ]
    MARCAS = [
        "Polymaker", "Bambu", "Hatchbox", "Creality", "Anycubic",
        "F3D", "Elegoo", "eSUN", "MultiLaser", "Yousu", "Volt3D"
    ]

    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLE_SHEET)
        self._filament: FilamentData | None = None
        self.setFixedWidth(320)
        self.setObjectName("FilamentForm")
        root = self._setup_layout(QVBoxLayout, (16,16,16,16), 4)
        self.setLayout(root)
        self.form_title = QLabel("Novo filamento")
        self.form_title.setObjectName("MenuTitle")
        self.tipo_combo = styled_combo(sorted(self.TIPOS))
        self.acabamento_combo = styled_combo(sorted(self.ACABAMENTOS))
        self.MARCAS = sorted(self.MARCAS)
        self.MARCAS.append("Outras")
        self.marca_combo = styled_combo(self.MARCAS)
        self.cor_input = styled_input("Ex: Azul royal")
        self.cor_hex_input = styled_input("#000000")
        self.pick_btn = ColoredDot()
        self.preco_input = styled_input("89,90")
        self.quantidade_input = QSpinBox()
        self.date_opened = QDateEdit(calendarPopup=True)
        self.date_opened.setFixedHeight(28)
        self.valid_date = QDateEdit(calendarPopup=True)
        self.valid_date.setFixedHeight(28)
        self.cancel_btn = QPushButton("Cancelar")
        self.save_btn = QPushButton("Salvar")
        root.addWidget(self.form_title)
        root.addWidget(make_divider())

        row1 = self._create_row1_layout()
        root.addLayout(row1)

        root.addWidget(form_label("Nome da cor"))
        root.addWidget(self.cor_input)
        color_row = self._create_colorrow_layout()
        root.addLayout(color_row)

        preco_quant_row =self._create_price_stock_layout()
        root.addLayout(preco_quant_row)

        dates_layout = self._setup_date_section()
        root.addLayout(dates_layout)

        row2 = self._create_bobin_weight()
        root.addLayout(row2)
        root.addStretch()
        root.addWidget(make_divider())

        btn_row = self._create_btn_row()
        root.addLayout(btn_row)

    def _create_bobin_weight(self):
        row2 = self._setup_layout(QHBoxLayout, spacing=8)
    
        inputs_config = [
            ("bobina_input", "Peso bobina (g)", "1000"),
            ("usado_input", "Já usado (g)", "0")
        ]

        for attr_name, label_text, default_val in inputs_config:
            column = self._setup_layout(QVBoxLayout, spacing=4)
            column.addWidget(form_label(label_text))
            input_widget = styled_input(default_val)
            setattr(self, attr_name, input_widget)
            column.addWidget(input_widget)
            row2.addLayout(column)
        return row2
    
    def _create_btn_row(self):
        btn_row = self._setup_layout(QHBoxLayout, spacing=8)
        self._setup_buttons(self.cancel_btn, "FilamentCancelButton", 32, self.cancelled.emit)
        self._setup_buttons(self.save_btn, "FilamentSaveButton", 32, self._on_save)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        return btn_row

    def _create_colorrow_layout(self):
        cor_row = self._setup_layout(QHBoxLayout, spacing=8)
        cor_column = self._setup_layout(QVBoxLayout, spacing=4)
        self._setup_coloreddot("#000000", 32, 42, self._pick_color)
        self.cor_hex_input.textChanged.connect(self._on_hex_changed)
        cor_column.addWidget(form_label("Cor (hex)"))
        cor_column.addWidget(self.cor_hex_input)
        cor_row.addWidget(self.pick_btn)
        cor_row.addLayout(cor_column)
        return cor_row

    def _create_price_stock_layout(self):
        preco_quant_row = self._setup_layout(QHBoxLayout, spacing=2)
        preco_column = self._setup_layout(QVBoxLayout, spacing=2)
        preco_column.addWidget(form_label("Preço/kg (R$)"))
        preco_column.addWidget(self.preco_input)
        preco_quant_row.addLayout(preco_column)
        quantidade_column = self._setup_layout(QVBoxLayout, spacing=2)
        quantidade_column.addWidget(form_label("Quantidade"))
        self._setup_spinbox()
        quantidade_column.addWidget(self.quantidade_input)
        preco_quant_row.addLayout(quantidade_column)
        return preco_quant_row

    def _create_row1_layout(self):
        row1 = self._setup_layout(QHBoxLayout, spacing=8)
        items = [
            (self.tipo_combo, "Tipo"),
            (self.acabamento_combo, "Acabamento"),
            (self.marca_combo, "Marca")
        ]

        for widget, label_text in items:
            column = self._setup_layout(QVBoxLayout, spacing=4)
            column.addWidget(form_label(label_text))
            column.addWidget(widget)
            row1.addLayout(column)
        return row1

    def _setup_buttons(self, button, objectname: str=None, height:int=24, callback=None):
        if objectname:
            button.setObjectName(objectname)
        button.setFixedHeight(height)
        if callback:
            button.clicked.connect(callback)

    def _setup_coloreddot(self, color, width, height, callback):
        self.pick_btn.handle_data(color)
        self.pick_btn.setFixedSize(width, height)
        self.pick_btn.clicked.connect(callback)

    def _setup_date_section(self):
        min_date = QDate(2024, 5, 1)
        dates_layout = self._setup_layout(QHBoxLayout, spacing=8)

        date_fields = [
            (self.date_opened, "Aberto em:"),
            (self.valid_date, "Válido até:")
        ]

        for widget, label_text in date_fields:
            widget.setDisplayFormat("dd-MM-yyyy")
            widget.setMinimumDate(min_date)
            column = self._setup_layout(QVBoxLayout, spacing=4)
            column.addWidget(form_label(label_text))
            column.addWidget(widget)
            dates_layout.addLayout(column)
        return dates_layout
        
    def _setup_layout(
        self, layout, margins=(0, 0, 0, 0), spacing=0, addstretch=False):
        lout = layout()
        lout.setContentsMargins(*margins)
        lout.setSpacing(spacing)
        if addstretch:
            lout.addStretch()
        return lout
    
    def _setup_spinbox(self):
        self.quantidade_input.setFixedHeight(28)
        self.quantidade_input.setMinimum(1)
        self.quantidade_input.setSuffix(' Bobinas')

    def _populate_form(self, filament):
        if filament:
            self.form_title.setText("Editar filamento")
            self.tipo_combo.setCurrentText(filament.tipo)
            self.marca_combo.setCurrentText(filament.marca)
            self.cor_input.setText(filament.cor)
            self.cor_hex_input.setText(filament.cor_str)
            self.preco_input.setText(
                f"{filament.preco_kg:.2f}".replace(".", ","))
            self.quantidade_input.setValue(filament.quantidade)
            self.bobina_input.setText(str(int(filament.peso_bobina_g)))
            self.usado_input.setText(str(int(filament.peso_usado_g)))
        else:
            self._clear()
           

    def load(self, filament: FilamentData | None):
        """Popula o formulário. None = novo filamento."""
        self._filament = filament
        self._populate_form(filament)

    def _pick_color(self, color_str):
        if QColor(color_str).isValid():
            self.cor_hex_input.setText(color_str)

    def _on_hex_changed(self, text):
        if QColor(text).isValid():
            self.pick_btn.handle_data(text)
    
    def _clear(self):
        self.form_title.setText("Novo filamento")
        self.tipo_combo.setCurrentIndex(0)
        self.marca_combo.setCurrentIndex(0)
        self.cor_input.clear()
        self.cor_hex_input.clear()
        self.preco_input.clear()
        self.bobina_input.clear()
        self.usado_input.clear()
        self.date_opened.clear()

    def _on_save(self):
        try:
            preco = float(self.preco_input.text().replace(",", "."))
            bobina = float(self.bobina_input.text().replace(",", "."))
            usado = float(self.usado_input.text().replace(",", "."))
        except ValueError:
            self._show_worning(
                "Valor inválido",
                "Preço, peso da bobina e peso usado devem ser numéricos.")
            return

        if self._filament is None:
            self._filament = FilamentData()

        filamento = self._set_filament_data(preco, bobina, usado)
        self._clear()
        self.saved.emit(filamento)
    
    def _show_worning(self, title):
        StyledMessageBox.warning(self, title, message)

    def _set_filament_data(self, preco, bobina, usado):
        self._filament.tipo = self.tipo_combo.currentText()
        self._filament.marca = self.marca_combo.currentText()
        self._filament.acabamento = self.acabamento_combo.currentText()
        self._filament.cor = self.cor_input.text().strip() or "Sem nome"
        self._filament.cor_str = self.cor_hex_input.text().strip()
        self._filament.quantidade = self.quantidade_input.value()
        self._filament.dat_abertura = self.date_opened.date().toString("dd/MM/yyyy")
        self._filament.data_validade = self.valid_date.date().toString("dd/MM/yyyy")
        self._filament.preco_kg = preco
        self._filament.peso_bobina_g = bobina
        self._filament.peso_usado_g = usado
        return self._filament


class FilamentCardRow(QWidget):
    edit_requested   = Signal(object)
    delete_requested = Signal(object)

    def __init__(self, filamento: FilamentData):
        super().__init__()
        self.filament = filamento

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)
        root.setAlignment(Qt.AlignVCenter)

        self.card = FilamentCard(filamento)
        root.addWidget(self.card, stretch=1)

        self.edit_btn = QPushButton("✎ Editar")
        self.edit_btn.setFixedSize(80, 30)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background: #E6F1FB; color: #185FA5;
                border: none; border-radius: 6px; font-size: 12px;
            }
            QPushButton:hover { background: #B5D4F4; }
        """)

        self.delete_btn = QPushButton("✕ Deletar")
        self.delete_btn.setFixedSize(80, 30)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background: #FAECE7; color: #993C1D;
                border: none; border-radius: 6px; font-size: 12px;
            }
            QPushButton:hover { background: #F5C6B0; }
        """)

        self.edit_btn.clicked.connect(
            lambda: self.edit_requested.emit(self.filament)
        )
        self.delete_btn.clicked.connect(
            lambda: self.delete_requested.emit(self.filament)
        )
        btn_col = QVBoxLayout()
        btn_col.setSpacing(6)
        btn_col.setAlignment(Qt.AlignVCenter)  # centraliza no eixo vertical
        btn_col.addWidget(self.edit_btn)
        btn_col.addWidget(self.delete_btn)
        root.addLayout(btn_col)


class FilamentPageWidget(QWidget):
    """Página que mostra os filamentos disponíveis e permite ações sobre eles"""

    def __init__(self):
        super().__init__()
        self._filaments: list[FilamentData] = []
        self._cards: list[FilamentCard] = []
        
        self._init_compontents()
        self._setup_styles()
        self._mount_layouts()
        self._connect_signals()
    
    def _connect_signals(self):
        self.form.saved.connect(self._on_form_saved)
        self.form.cancelled.connect(self._close_form)
        self.add_btn.clicked.connect(self._on_new)

    def _init_compontents(self):
        self.add_btn = QPushButton("+ Novo filamento")
        self.edit_btn = QPushButton("Editar")
        self.delete_btn = QPushButton("Deletar")
        self.list_container = QWidget()
        
        self.empty_lbl = QLabel(
            "Nenhum filamento cadastrado.\nClique em \"+ Novo filamento\""
        )
        self.form = FilamentForm()
        self.form.hide()
    
    def _mount_layouts(self):
        root_layout = self._setup_layout(QHBoxLayout)
        self.setLayout(root_layout)
        left = self._setup_layout(QVBoxLayout)
        topbar = self._set_topbar("FilamentTopBar", 56)
        topbar_layout = self._setup_layout(QHBoxLayout, (20, 0, 20, 0))
        topbar.setLayout(topbar_layout)
        title = QLabel("Filamentos")
        title.setObjectName("MenuTitle")
        topbar_layout.addWidget(title)
        topbar_layout.addStretch()
        topbar_layout.addWidget(self.add_btn)
        left.addWidget(topbar)
        scroll = self._setup_scrollarea()
        scroll.setWidget(self.list_container)
        left.addWidget(scroll)
        self.list_layout = self._setup_layout(
            QVBoxLayout, margins=(16, 8, 16, 8), spacing=8)
        self.list_container.setLayout(self.list_layout)
        self.empty_lbl.setAlignment(Qt.AlignCenter)
        self.empty_lbl.setObjectName("MenuSubtitle")
        self.list_layout.insertWidget(0, self.empty_lbl)
        self.list_layout.addStretch()
        left_widget = QWidget()
        left_widget.setLayout(left)
        root_layout.addWidget(left_widget, stretch=1)
        root_layout.addWidget(self.form)

    def _setup_buttons(self, button, objectname: str=None, height:int=24):
        if objectname:
            button.setObjectName(objectname)
        button.setFixedHeight(height)

    def _setup_layout(
        self, layout, margins=(0, 0, 0, 0), spacing=0, addstretch=False):
        lout = layout()
        lout.setContentsMargins(*margins)
        lout.setSpacing(spacing)
        if addstretch:
            lout.addStretch()
        return lout
    
    def _setup_scrollarea(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: #F5F4F0;")
        return scroll

    def _setup_styles(self):
        self.setStyleSheet(STYLE_SHEET)
        self.list_container.setStyleSheet("background: #F5F4F0;")
        self._setup_buttons(self.add_btn, "FilamentNew", 32)
        self._setup_buttons(self.edit_btn, None, 32)

    def _set_topbar(self, objectname, height):
        topbar = QWidget()
        topbar.setObjectName(objectname)
        topbar.setFixedHeight(height)
        return topbar

    def _rebuild_list(self):
        """Reconstrói todos os cards a partir de self._filaments."""
        for card in self._cards:
            self.list_layout.removeWidget(card)
            card.deleteLater()
        self._cards.clear()
        self.empty_lbl.setVisible(len(self._filaments) == 0)

        for f in self._filaments:
            row = FilamentCardRow(f)
            row.edit_requested.connect(self._on_edit)
            row.delete_requested.connect(self._on_delete)
            self.list_layout.insertWidget(self.list_layout.count() - 1, row)
            self._cards.append(row)

    def _on_new(self):
        if self.form.isHidden():
            self.form.load(None)
            self.form.show()

    def _on_edit(self, filament: FilamentData):
        self.form.load(filament)
        self.form.show()

    def _on_delete(self, filament: FilamentData):
        reply = QMessageBox.question(
            self, "Excluir filamento",
            f"Excluir {filament.marca} {filament.tipo} ({filament.cor})?",
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._filaments.remove(filament)
            self._rebuild_list()

    def _on_form_saved(self, filament: FilamentData):
        if filament not in self._filaments:
            self._filaments.append(filament)
        self._rebuild_list()
        self._close_form()

    def _close_form(self):
        self.form.hide()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
