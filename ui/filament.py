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

INPUT_HEIGHT = 28

class _T:
    """Paleta e métricas compartilhadas entre os widgets."""
    # Cores base
    BG         = "#F5F4F0"
    SURFACE    = "#FFFFFF"
    BORDER     = "#E2E0DA"
    TEXT       = "#1A1A1A"
    MUTED      = "#6B6860"
 
    # Ação primária (azul)
    PRIMARY    = "#185FA5"
    PRIMARY_BG = "#E6F1FB"
    PRIMARY_HV = "#B5D4F4"
 
    # Ação destrutiva (vermelho)
    DANGER     = "#993C1D"
    DANGER_BG  = "#FAECE7"
    DANGER_HV  = "#F5C6B0"
 
    # Medidas
    RADIUS     = "8px"
    FONT_SM    = "11px"
    FONT_MD    = "12px"
    BTN_H      = 30
    INPUT_H    = 28
    

_EDIT_BTN_STYLE = f"""
    QPushButton {{
        background: {_T.PRIMARY_BG}; color: {_T.PRIMARY};
        border: none; border-radius: {_T.RADIUS}; font-size: {_T.FONT_MD};
        font-weight: 600;
    }}
    QPushButton:hover {{ background: {_T.PRIMARY_HV}; }}
    QPushButton:pressed {{ background: #8EC0EE; }}
"""
 
_DELETE_BTN_STYLE = f"""
    QPushButton {{
        background: {_T.DANGER_BG}; color: {_T.DANGER};
        border: none; border-radius: {_T.RADIUS}; font-size: {_T.FONT_MD};
        font-weight: 600;
    }}
    QPushButton:hover {{ background: {_T.DANGER_HV}; }}
    QPushButton:pressed {{ background: #EDA07A; }}
"""

class LayoutMixin:
    """Utilitário de layout reutilizável."""
 
    @staticmethod
    def make_layout(
        layout_cls,
        margins: tuple[int, int, int, int] = (0, 0, 0, 0),
        spacing: int = 0,
        stretch: bool = False,
    ):
        lout = layout_cls()
        lout.setContentsMargins(*margins)
        lout.setSpacing(spacing)
        if stretch:
            lout.addStretch()
        return lout
 
    @staticmethod
    def make_labeled_column(label_text: str, widget: QWidget, spacing: int = 4):
        """Coluna vertical label + widget, padrão recorrente no formulário."""
        col = QVBoxLayout()
        col.setSpacing(spacing)
        col.addWidget(form_label(label_text))
        col.addWidget(widget)
        return col


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
        self.filament_data_validade.setText(self.filament.data_validade)
        self.progress_bar.setValue(value)
        self._update_progressbar_text_color(value)    


class FilamentForm(QWidget, LayoutMixin):
    """Formulário lateral para criar ou editar um FilamentData."""
    saved = Signal(object)  # emite o FilamentData salvo
    cancelled = Signal()

    TIPOS = sorted([
        "PLA", "PETG", "ABS", "TPU", "ASA", "Nylon", "HIPS"
    ])
    ACABAMENTOS = sorted([
        "Hyper Speed", "Matte", "Silk", "Metalizado", "Sólido",
        "Condutivo", "Premium", "Velvet"
    ])
    _MARCAS_BASE = sorted([
        "Polymaker", "Bambu", "Hatchbox", "Creality", "Anycubic",
        "F3D", "Elegoo", "eSUN", "MultiLaser", "Yousu", "Volt3D",
    ])
    MARCAS = _MARCAS_BASE + ["Outras"]

    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLE_SHEET)
        self._filament: FilamentData | None = None
        self.setFixedWidth(330)
        self.setObjectName("FilamentForm")
        self._build_widgets()
        self._build_layout()
        self._connect_signals()

    def _build_widgets(self):
        self.form_title = QLabel("Novo filamento", objectName="MenuTitle")
        self.tipo_combo = styled_combo(sorted(self.TIPOS))
        self.acabamento_combo = styled_combo(sorted(self.ACABAMENTOS))
        self.marca_combo = styled_combo(self.MARCAS)
        self.cor_input = styled_input("Ex: Azul royal")
        self.cor_hex_input = styled_input("#000000")
        self.pick_btn = ColoredDot()
        self.pick_btn.handle_data("#000000")
        self.pick_btn.setFixedSize(32, INPUT_HEIGHT + 4)
        self.preco_input = styled_input("89,90")
        self.bobina_input = styled_input("100")
        self.usado_input = styled_input("0")
        self.quantidade_input = QSpinBox()
        self.quantidade_input.setFixedHeight(INPUT_HEIGHT)
        self.quantidade_input.setMinimum(1)
        self.quantidade_input.setSuffix(' Bobinas')
        self.date_opened = self._make_date_edit()
        self.valid_date = self._make_date_edit()
        self.cancel_btn = QPushButton("✕  Cancelar", objectName="FilamentCancelButton")
        self.cancel_btn.setFixedHeight(34)
        self.save_btn = QPushButton("✔  Salvar", objectName="FilamentSaveButton")
        self.save_btn.setFixedHeight(34)

    def _build_layout(self):
        root = self.make_layout(QVBoxLayout, (16,16,16,16), spacing=10)
        self.setLayout(root)
        
        root.addWidget(self.form_title)
        root.addWidget(make_divider())

        row1 = self.make_layout(QHBoxLayout, spacing=8)
        for widget, label in (
            (self.tipo_combo, "Tipo"),
            (self.acabamento_combo, "Acabamento"),
            (self.marca_combo, "Marca"),
        ):
            row1.addLayout(self.make_labeled_column(label, widget))
        root.addLayout(row1)

        root.addLayout(self.make_labeled_column("Nome da cor", self.cor_input))
        cor_row = self.make_layout(QHBoxLayout, spacing=4)
        cor_row.addWidget(self.pick_btn)
        cor_row.addLayout(self.make_labeled_column("Cor (hex)", self.cor_hex_input))
        root.addLayout(cor_row)

        preco_quant_row = self.make_layout(QHBoxLayout, spacing=8)
        preco_quant_row.addLayout(self.make_labeled_column("Preço/kg (R$)", self.preco_input))
        preco_quant_row.addLayout(self.make_labeled_column("Quantidade", self.quantidade_input))
        root.addLayout(preco_quant_row)

        date_row = self.make_layout(QHBoxLayout, spacing=8)
        for widget, label in (
            (self.date_opened, "Aberto em"),
            (self.valid_date,  "Válido até"),
        ):
            date_row.addLayout(self.make_labeled_column(label, widget))
        root.addLayout(date_row)

        # Pesos
        weight_row = self.make_layout(QHBoxLayout, spacing=8)
        weight_row.addLayout(self.make_labeled_column("Peso bobina (g)", self.bobina_input))
        weight_row.addLayout(self.make_labeled_column("Já usado (g)",    self.usado_input))
        root.addLayout(weight_row)
 
        root.addStretch()
        root.addWidget(make_divider())
 
        # Botões
        btn_row = self.make_layout(QHBoxLayout, spacing=8)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        root.addLayout(btn_row)
 
    def _connect_signals(self):
        self.cancel_btn.clicked.connect(self.cancelled.emit)
        self.save_btn.clicked.connect(self._on_save)
        self.pick_btn.clicked.connect(self._pick_color)
        self.cor_hex_input.textChanged.connect(self._on_hex_changed)
    
    @staticmethod
    def _make_date_edit() -> QDateEdit:
        d = QDateEdit(calendarPopup=True)
        d.setDisplayFormat("dd-MM-yyyy")
        d.setMinimumDate(QDate(2024, 5, 1))
        d.setDate(QDate.currentDate())
        d.setFixedHeight(INPUT_HEIGHT)
        return d
        
    def _populate_form(self, filament):
        if filament is None:
            self._clear()
            return

        self.form_title.setText("Editar filamento")
        self.tipo_combo.setCurrentText(filament.tipo)
        self.marca_combo.setCurrentText(filament.marca)
        self.acabamento_combo.setCurrentText(filament.acabamento) 
        self.cor_input.setText(filament.cor)
        self.cor_hex_input.setText(filament.cor_str)
        self.preco_input.setText(
            f"{filament.preco_kg:.2f}".replace(".", ","))
        self.quantidade_input.setValue(filament.quantidade)
        self.bobina_input.setText(str(int(filament.peso_bobina_g)))
        self.usado_input.setText(str(int(filament.peso_usado_g)))
        if filament.dat_abertura:
            self.date_opened.setDate(
                QDate.fromString(filament.dat_abertura, "dd/MM/yyyy"))
        if filament.data_validade:
            self.valid_date.setDate(
                QDate.fromString(filament.data_validade, "dd/MM/yyyy"))    

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
            self._show_warning(
                "Valor inválido",
                "Preço, peso da bobina e peso usado devem ser numéricos.")
            return

        if self._filament is None:
            self._filament = FilamentData()

        filamento = self._set_filament_data(preco, bobina, usado)
        self._clear()
        self.saved.emit(filamento)
    
    def _show_warning(self, title, message):
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
 
    _BTN_W, _BTN_H = 88, _T.BTN_H
 
    def __init__(self, filamento: FilamentData):
        super().__init__()
        self.filament = filamento
 
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)
        root.setAlignment(Qt.AlignVCenter)
 
        card = FilamentCard(filamento)
        root.addWidget(card, stretch=1)
 
        # Botões — estilos movidos para constantes de módulo
        self.edit_btn   = self._make_button("✎  Editar",  _EDIT_BTN_STYLE)
        self.delete_btn = self._make_button("✕  Deletar", _DELETE_BTN_STYLE)
 
        self.edit_btn.clicked.connect(
            lambda: self.edit_requested.emit(self.filament))
        self.delete_btn.clicked.connect(
            lambda: self.delete_requested.emit(self.filament))
 
        btn_col = QVBoxLayout()
        btn_col.setSpacing(6)
        btn_col.setAlignment(Qt.AlignVCenter)
        btn_col.addWidget(self.edit_btn)
        btn_col.addWidget(self.delete_btn)
        root.addLayout(btn_col)
 
    def _make_button(self, text: str, style: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedSize(self._BTN_W, self._BTN_H)
        btn.setStyleSheet(style)
        return btn


class FilamentPageWidget(QWidget, LayoutMixin):
    """Página que mostra os filamentos disponíveis e permite ações sobre eles"""

    def __init__(self):
        super().__init__()
        self._filaments: list[FilamentData] = []
        self._rows: list[FilamentCardRow] = []
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
        self.add_btn.setObjectName("PrimaryButton")
        self.edit_btn = QPushButton("Editar")
        self.delete_btn = QPushButton("Deletar")
        self.list_container = QWidget()
        
        self.empty_lbl = QLabel(
            "Nenhum filamento cadastrado.\nClique em \"+ Novo filamento\""
        )
        self.form = FilamentForm()
        self.form.hide()
    
    def _mount_layouts(self):
        root_layout = self.make_layout(QHBoxLayout)
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
        """Remove widgets antigos e insere os novos sem recriar o layout."""
        for row in self._rows:
            self.list_layout.removeWidget(row)
            row.deleteLater()
        self._rows.clear()
 
        has_items = bool(self._filaments)
        self.empty_lbl.setVisible(not has_items)
        insert_pos = self.list_layout.count() - 1
        for f in self._filaments:
            row = FilamentCardRow(f)
            row.edit_requested.connect(self._on_edit)
            row.delete_requested.connect(self._on_delete)
            self.list_layout.insertWidget(insert_pos, row)
            insert_pos += 1
            self._rows.append(row)

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
