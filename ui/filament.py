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

        self.name_lbl = QLabel("Filamento", objectName="CardTitle")
        self.filament_type = QLabel("PLA")
        self.filament_acabamento = QLabel("Hyper Speed")
        self.filament_brand = QLabel("Anycubic")
        self.filament_price = QLabel("R$ 89,90")
        self.filament_color = ColoredDot()
        self.filament_color.handle_data("#2563EB")
        self.filament_color.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.filament_color.setFixedSize(40, 40)
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
        grid.addWidget(form_label("Preço/kg"), 0, 3)
        grid.addWidget(self.filament_price, 1, 3)
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
        self.progress_bar.setStyleSheet(
            "QProgressBar {"
            " border-radius: 4px;"
            " background: #E5E5E3;"
            " text-align: center;"
            " font-size: 10px;"
            "}"
            "QProgressBar::chunk {"
            f" background: {self._chunk_color};"
            " border-radius: 4px;"
            "}"
        )

    def _update_progressbar_text_color(self, value: int):
        """Troca a cor do texto para contraste com o chunk."""
        # acima de 50% o texto fica sobre o chunk (azul) → branco
        # abaixo de 50% o texto fica sobre o fundo (cinza) → preto
        text_color = "white" if value > 50 else "#2C2C2A"
        if self._chunk_color == "#ffffff":
            text_color = "black"
        elif self._chunk_color == "#000000":
            text_color = "white"
        
        self.progress_bar.setStyleSheet(
            "QProgressBar {"
            " border-radius: 4px;"
            " background: #E5E5E3;"
            f" color: {text_color};"
            " text-align: center;"
            " font-size: 10px;"
            "}"
            "QProgressBar::chunk {"
            " border-radius: 4px;"
            f" background: {self._chunk_color};"
            "}"
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
        self.progress_bar.setValue(value)
        # chama explicitamente — setValue pode não disparar valueChanged
        # se o valor for igual ao anterior
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
        "F3D", "Elegoo", "eSUN", "MultiLaser", "Yousu", "Outra"
    ]

    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLE_SHEET)
        self._filament: FilamentData | None = None
        self.setFixedWidth(320)
        self.setObjectName("FilamentForm")

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(4)

        self.form_title = QLabel("Novo filamento")
        self.form_title.setObjectName("MenuTitle")

        self.tipo_combo = styled_combo(sorted(self.TIPOS))
        self.acabamento_combo = styled_combo(sorted(self.ACABAMENTOS))
        self.marca_combo = styled_combo(sorted(self.MARCAS))
        self.cor_input = styled_input("Ex: Azul royal")
        self.cor_hex_input = styled_input("#000000")
        self.pick_btn = ColoredDot()
        self.preco_input = styled_input("89,90")
        self.quantidade_input = QSpinBox()
        self.date_opened = QDateEdit(calendarPopup=True)
        self.valid_date = QDateEdit(calendarPopup=True)
        self.cancel_btn = QPushButton("Cancelar")
        self.save_btn = QPushButton("Salvar")

        root.addWidget(self.form_title)
        root.addWidget(make_divider())

        # tipo + marca
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        c1 = QVBoxLayout()
        c1.setSpacing(4)
        c1.addWidget(form_label("Tipo"))
        c1.addWidget(self.tipo_combo)

        c2 = QVBoxLayout()
        c2.setSpacing(4)
        c2.addWidget(form_label("Acabamento"))
        c2.addWidget(self.acabamento_combo)

        c3 = QVBoxLayout()
        c3.setSpacing(4)
        c3.addWidget(form_label("Marca"))
        c3.addWidget(self.marca_combo)

        row1.addLayout(c1)
        row1.addLayout(c2)
        row1.addLayout(c3)
        root.addLayout(row1)

        # nome da cor
        root.addWidget(form_label("Nome da cor"))
        root.addWidget(self.cor_input)

        # cor hex (color picker)
        cor_row = QHBoxLayout()
        cor_row.setSpacing(2)
        cor_columun = QVBoxLayout()
        cor_columun.setSpacing(2)
        cor_columun.addWidget(form_label("Cor (hex)"))
        
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
        preco_column.addWidget(self.preco_input)
        preco_quant_row.addLayout(preco_column)

        quantidade_column = QVBoxLayout()
        quantidade_column.setSpacing(2)
        quantidade_column.addWidget(form_label("Quantidade"))
        self.quantidade_input.setFixedHeight(28)
        self.quantidade_input.setMinimum(1)
        self.quantidade_input.setSuffix(' Bobinas')
        quantidade_column.addWidget(self.quantidade_input)
        preco_quant_row.addLayout(quantidade_column)
        root.addLayout(preco_quant_row)

        #data de abertura e vencimento da bobina:
        self.date_opened.setDisplayFormat("dd-MM-yyyy")
        self.date_opened.setMinimumDate(QDate(2024, 5, 1))
        self.valid_date.setDisplayFormat("dd-MM-yyyy")
        self.valid_date.setMinimumDate(QDate(2024, 5, 1))
        dates_layout = QHBoxLayout()
        dates_layout.setSpacing(8)
        open_date_column = QVBoxLayout()
        open_date_column.setSpacing(4)
        open_date_column.addWidget(form_label("Aberto em:"))
        open_date_column.addWidget(self.date_opened)
        dates_layout.addLayout(open_date_column)
        valid_date_column = QVBoxLayout()
        valid_date_column.setSpacing(4)
        valid_date_column.addWidget(form_label("Válido até:"))
        valid_date_column.addWidget(self.valid_date)
        dates_layout.addLayout(valid_date_column)
        root.addLayout(dates_layout)

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
        self.cancel_btn.setFixedHeight(32)
        self.cancel_btn.setObjectName("FilamentCancelButton")
        self.save_btn.setFixedHeight(32)
        self.save_btn.setObjectName("FilamentSaveButton")
        self.cancel_btn.clicked.connect(self.cancelled.emit)
        self.save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        root.addLayout(btn_row)

    def _populate_form(self, filament):
        if filament is None:
            self._clear()
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
    
    def _clear(self):
        self.form_title.setText("Novo filamento")
        self.tipo_combo.setCurrentIndex(0)
        self.marca_combo.setCurrentIndex(0)
        self.cor_input.clear()
        self.cor_hex_input.clear()
        self.preco_input.clear()
        self.bobina_input.clear()
        self.usado_input.clear()

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
        self._clear()
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


class FilamentCardRow(QWidget):
    edit_requested   = Signal(object)
    delete_requested = Signal(object)

    def __init__(self, filamento: FilamentData):
        super().__init__()
        self.filament = filamento

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)
        # alinha todos os filhos ao centro vertical
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
        self.setStyleSheet(STYLE_SHEET)

        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(0)

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
        
        self.edit_btn = QPushButton("Editar")
        self.edit_btn.setFixedHeight(32)
        self.delete_btn = QPushButton("Deletar")
        self.delete_btn.setFixedHeight(32)

        self.add_btn.clicked.connect(self._on_new)

        tb.addWidget(title)
        tb.addStretch()
        tb.addWidget(self.add_btn)
        left.addWidget(topbar)

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

        self.form = FilamentForm()
        self.form.hide()
        self.form.saved.connect(self._on_form_saved)
        self.form.cancelled.connect(self._close_form)
        root_layout.addWidget(self.form)

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
