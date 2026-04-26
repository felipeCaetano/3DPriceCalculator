from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (
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


class FilamentCard(QFrame):
    """Card Filamento"""
    edit_requested = Signal(object)  # emite o FilamentData salvo
    delete_requested = Signal()

    def __init__(self, filamento: FilamentData):
        super().__init__()
        self.filament = filamento
        self.setProperty("class", "Card")
        fil_lay = QVBoxLayout(self)
        fil_lay.setSpacing(2)
        fil_lay.setContentsMargins(4,4,4,4)
        self.name_lbl = QLabel("Filamento", objectName="CardTitle")
        fil_lay.addWidget(self.name_lbl)

        f_grid = QGridLayout()
        f_grid.setHorizontalSpacing(12)
        f_grid.setVerticalSpacing(4)

        f_grid.addWidget(form_label("Tipo"), 0, 0)
        self.filament_type =QLabel("PLA")
        f_grid.addWidget(self.filament_type, 1, 0)
        f_grid.addWidget(form_label("Marca"), 0, 1)
        self.filament_brand = QLabel("Anycubic")

        f_grid.addWidget(self.filament_brand, 1, 1)
        f_grid.addWidget(form_label("Cor"), 0, 2)
        self.filament_color = ColoredDot()
        self.filament_color.handle_data("#0000ff")
        self.filament_color.setFixedSize(32, 32)
        f_grid.addWidget(self.filament_color, 1, 2)
        f_grid.addWidget(form_label("Preço/kg"), 0, 3)
        self.filament_price = QLabel("R$ 89,90")
        f_grid.addWidget(self.filament_price, 1, 3)
        fil_lay.addLayout(f_grid)

        fil_lay.addWidget(form_label("Bobina restante:"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(64)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(16)
        self.progress_bar.setStyleSheet(
            """QProgressBar::chunk {
             background-color: #2563EB;
             border-radius: 4px; }"""
        )
        fil_lay.addWidget(self.progress_bar)

        if filamento:
            self.refresh()

    def _apply_dot_color(self, hex_color: str):
        color = hex_color if hex_color else "#888780"
        self.color_dot.setStyleSheet(
            f"background: {color}; border-radius: 16px;"
            " border: 0.5px solid #D3D1C7;")

    @staticmethod
    def _icon_btn(icon, color, bg):
        btn = QPushButton(icon)
        btn.setFixedSize(26, 26)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {bg}; color: {color};
                border: none; border-radius: 6px;
                font-size: 13px;
            }}
            QPushButton:hover {{ opacity: 0.8; }}
        """)
        return btn

    def refresh(self):
        """Atualiza o card com os dados atuais do filament."""
        self.name_lbl.setText(
            f"{self.filament.marca} — {self.filament.tipo} "
        f"{self.filament.acabamento}: {self.filament.cor}"
        )
        self.filament_price.setText(str(self.filament.preco_kg))
        self.filament_price.setReadOnly(True)
        self.filament_color.handle_data(self.filament.cor_str)
        self.filament_brand.setText(self.filament.marca)
        self.progress_bar.setValue(self.filament.bobina_restante_pct)
        self.filament_type.setText((self.filament.tipo))
        self.progress_bar.setStyleSheet(
            f"""QProgressBar::chunk {{
             background-color: {self.filament.cor_str};
             border-radius: 4px; 
             border-color: #ff0000;}}"""
        )


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
        "F3D", "Elegoo", "eSUN", "MultiLaser", "Yousu", "Outra"
    ]

    def __init__(self):
        super().__init__()
        self._filament: FilamentData | None = None
        self.setFixedWidth(320)
        self.setObjectName("FilamentForm")

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(4)

        self.form_title = QLabel("Novo filamento")
        self.form_title.setObjectName("MenuTitle")
        root.addWidget(self.form_title)
        root.addWidget(make_divider())

        # tipo + marca
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        c1 = QVBoxLayout()
        c1.setSpacing(4)
        c1.addWidget(form_label("Tipo"))
        self.tipo_combo = styled_combo(sorted(self.TIPOS))
        c1.addWidget(self.tipo_combo)

        c2 = QVBoxLayout()
        c2.setSpacing(4)
        c2.addWidget(form_label("Acabamento"))
        self.acabamento_combo = styled_combo(sorted(self.ACABAMENTOS))
        c2.addWidget(self.acabamento_combo)

        c3 = QVBoxLayout()
        c3.setSpacing(4)
        c3.addWidget(form_label("Marca"))
        self.marca_combo = styled_combo(sorted(self.MARCAS))
        c3.addWidget(self.marca_combo)

        row1.addLayout(c1)
        row1.addLayout(c2)
        row1.addLayout(c3)
        root.addLayout(row1)

        # nome da cor
        root.addWidget(form_label("Nome da cor"))
        self.cor_input = styled_input("Ex: Azul royal")
        root.addWidget(self.cor_input)

        # cor hex (color picker)
        cor_row = QHBoxLayout()
        cor_row.setSpacing(2)
        cor_columun = QVBoxLayout()
        cor_columun.setSpacing(2)
        cor_columun.addWidget(form_label("Cor (hex)"))
        self.cor_hex_input = styled_input("#000000")

        self.pick_btn = ColoredDot()
        self.pick_btn.handle_data("#000000")
        self.pick_btn.setFixedSize(32, 42)
        self.pick_btn.clicked.connect(self._pick_color)
        self.cor_hex_input.textChanged.connect(self._on_hex_changed)

        cor_row.addWidget(self.pick_btn)
        cor_columun.addWidget(self.cor_hex_input)
        cor_row.addLayout(cor_columun)
        root.addLayout(cor_row)

        # preço/kg e quantidade
        preco_quant_row = QHBoxLayout()
        preco_quant_row.setSpacing(2)
        preco_column =  QVBoxLayout()
        preco_column.setSpacing(2)
        preco_column.addWidget(form_label("Preço/kg (R$)"))
        self.preco_input = styled_input("89,90")
        preco_column.addWidget(self.preco_input)
        preco_quant_row.addLayout(preco_column)

        quantidade_column = QVBoxLayout()
        quantidade_column.setSpacing(2)
        quantidade_column.addWidget(form_label("Quantidade"))
        self.quantidade_input = QSpinBox()
        self.quantidade_input.setStyleSheet("""
                QSpinBox {
                    border: 0.5px solid #B4B2A9;
                    border-radius: 6px;
                    padding: 0 8px;
                    font-size: 12px;
                    background: white;
                    color: #2C2C2A;
                }
                QSpinBox:focus { border-color: #185FA5; }
                QSpinBox:up-button { subcontrol-origin border;
                width: 18px; }
                QSpinBox:down-button { subcontrol-origin border;
                width: 18px; }
            """)
        self.quantidade_input.setFixedHeight(28)
        self.quantidade_input.setMinimum(1)
        self.quantidade_input.setSuffix(' Bobinas')
        quantidade_column.addWidget(self.quantidade_input)
        preco_quant_row.addLayout(quantidade_column)
        root.addLayout(preco_quant_row)

        # peso bobina + peso usado
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        c3 = QVBoxLayout()
        c3.setSpacing(4)
        c3.addWidget(form_label("Peso bobina (g)"))
        self.bobina_input = styled_input("1000")
        c3.addWidget(self.bobina_input)

        c4 = QVBoxLayout()
        c4.setSpacing(4)
        c4.addWidget(form_label("Já usado (g)"))
        self.usado_input = styled_input("0")
        c4.addWidget(self.usado_input)

        row2.addLayout(c3)
        row2.addLayout(c4)
        root.addLayout(row2)

        root.addStretch()
        root.addWidget(make_divider())

        # botões
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setFixedHeight(32)
        self.cancel_btn.setObjectName("FilamentCancelButton")
        self.save_btn = QPushButton("Salvar")
        self.save_btn.setFixedHeight(32)
        self.save_btn.setObjectName("FilamentSaveButton")
        self.cancel_btn.clicked.connect(self.cancelled.emit)
        self.save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        root.addLayout(btn_row)

    def _populate_form(self, filament):
        if filament is None:
            self.form_title.setText("Novo filamento")
            self.tipo_combo.setCurrentIndex(0)
            self.marca_combo.setCurrentIndex(0)
            self.cor_input.clear()
            self.cor_hex_input.setPlaceholderText("#000000")
            self.preco_input.setPlaceholderText("89,90")
            self.bobina_input.setPlaceholderText("1000")
            self.usado_input.setPlaceholderText("0")
        else:
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

    def _on_save(self):
        try:
            preco = float(self.preco_input.text().replace(",", "."))
            bobina = float(self.bobina_input.text().replace(",", "."))
            usado = float(self.usado_input.text().replace(",", "."))
        except ValueError:
            StyledMessageBox.warning(
                self, "Valor inválido",
                "Preço, peso da bobina e peso usado devem ser numéricos.")
            return

        if self._filament is None:
            self._filament = FilamentData()

        filamento = self._set_filament_data(preco, bobina, usado)
        self.saved.emit(filamento)

    def _set_filament_data(self, preco, bobina, usado):
        self._filament.tipo = self.tipo_combo.currentText()
        self._filament.marca = self.marca_combo.currentText()
        self._filament.acabamento = self.acabamento_combo.currentText()
        self._filament.cor = self.cor_input.text().strip() or "Sem nome"
        self._filament.cor_str = self.cor_hex_input.text().strip()
        self._filament.quantidade = self.quantidade_input.value()
        self._filament.preco_kg = preco
        self._filament.peso_bobina_g = bobina
        self._filament.peso_usado_g = usado
        return self._filament


class FilamentPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._filaments: list[FilamentData] = []
        self._cards: list[FilamentCard] = []
        self.setStyleSheet(STYLE_SHEET)

        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # coluna esquerda — lista
        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(0)

        # topbar da página
        topbar = QWidget()
        topbar.setObjectName("FilamentTopBar")
        topbar.setFixedHeight(56)

        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(20, 0, 20, 0)
        title = QLabel("Filamentos")
        title.setObjectName("MenuTitle")
        self.add_btn = QPushButton("+ Novo filamento")
        self.add_btn.setObjectName("FilamentNew")
        self.add_btn.setFixedHeight(32)

        self.add_btn.clicked.connect(self._on_new)
        tb.addWidget(title)
        tb.addStretch()
        tb.addWidget(self.add_btn)
        left.addWidget(topbar)

        # área de scroll com os cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: #F5F4F0;")

        self.list_container = QWidget()
        self.list_container.setStyleSheet("background: #F5F4F0;")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(16, 8, 16, 8)
        self.list_layout.setSpacing(8)
        self.list_layout.addStretch()

        # estado vazio
        self.empty_lbl = QLabel(
            "Nenhum filamento cadastrado.\nClique em \"+ Novo filamento\""
        )
        self.empty_lbl.setAlignment(Qt.AlignCenter)
        self.empty_lbl.setObjectName("MenuSubtitle")
        self.list_layout.insertWidget(0, self.empty_lbl)

        scroll.setWidget(self.list_container)
        left.addWidget(scroll)

        left_widget = QWidget()
        left_widget.setLayout(left)
        root_layout.addWidget(left_widget, stretch=1)

        # coluna direita — formulário (começa escondida)
        self.form = FilamentForm()
        self.form.hide()
        self.form.saved.connect(self._on_form_saved)
        self.form.cancelled.connect(self._close_form)
        root_layout.addWidget(self.form)

    # ── lista ──
    def _rebuild_list(self):
        """Reconstrói todos os cards a partir de self._filaments."""
        # remove cards antigos
        for card in self._cards:
            self.list_layout.removeWidget(card)
            card.deleteLater()
        self._cards.clear()

        self.empty_lbl.setVisible(len(self._filaments) == 0)

        for f in self._filaments:
            card = FilamentCard(f)
            card.edit_requested.connect(self._on_edit)
            card.delete_requested.connect(self._on_delete)
            # insere antes do stretch
            self.list_layout.insertWidget(
                self.list_layout.count() - 1, card)
            self._cards.append(card)

    # ── ações ──
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
