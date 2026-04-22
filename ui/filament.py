from PySide6.QtCore import Qt, QPropertyAnimation, QSize, Signal
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (
    QColorDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMdiSubWindow,
    QMessageBox, QProgressBar, QPushButton, QScrollArea, QStyle, QStyleOption,
    QVBoxLayout, QWidget, QSizePolicy
)
 
from models.filament import FilamentData
from ui.stylehelper import form_label, make_divider, panel_title, styled_combo, \
    styled_input
from ui.styledmessagebox import StyledMessageBox


class FilamentCard(QFrame):
    """Card Filamento"""
    def __init__(self):
        super().__init__()
        self.setProperty("class", "Card")
        fil_lay = QVBoxLayout(self)
        fil_lay.addWidget(QLabel("Filamento", objectName="CardTitle"))
        
        f_grid = QGridLayout()
        f_grid.addWidget(QLabel("Tipo"), 0, 0)
        self.filament_type = styled_combo(
            ["PLA", "PETG", "ABS", "TPU", "ASA", "Nylon"]
        )
        f_grid.addWidget(self.filament_type, 1, 0)
        f_grid.addWidget(QLabel("Marca"), 0, 1)
        self.filament_brand = styled_combo(
            ["Elegoo", "Polymaker", "Bambu", "Hatchbox", "eSUN", "MultiLaser",
             "Creality", "Volt3D", "F3D", "GTMAX3D", "Anycubic"]
        )

        f_grid.addWidget(self.filament_brand, 1, 1)
        f_grid.addWidget(QLabel("Cor"), 2, 0)
        self.filament_color = styled_combo(
            ["Azul", "Vermelho", "Branco", "Preto", "Amarelo", "Verde"]
        )
        f_grid.addWidget(self.filament_color, 3, 0)
        f_grid.addWidget(QLabel("Preço/kg (R$)"), 2, 1)
        self.filament_price =QLineEdit()
        self.filament_price.setPlaceholderText("89,90")
        f_grid.addWidget(self.filament_price, 3, 1)
        fil_lay.addLayout(f_grid)
        
        fil_lay.addWidget(QLabel("Bobina restante: 62%"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(62)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #2563EB; border-radius: 4px; }")
        fil_lay.addWidget(self.progress_bar)

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
        self.name_lbl.setText(f"{self.filament.marca} — {self.filament.tipo}")
        self.cor_lbl.setText(self.filament.cor)
        self._apply_dot_color(self.filament.cor_str)


class FilamentForm(QWidget):
    """Formulário lateral para criar ou editar um FilamentData."""
    saved    = Signal(object)   # emite o FilamentData salvo
    cancelled = Signal()
 
    TIPOS  = ["PLA", "PETG", "ABS", "TPU", "ASA", "Nylon", "HIPS"]
    MARCAS = ["Polymaker", "Bambu", "Hatchbox", "eSUN", "Creality", "Outra"]
 
    def __init__(self):
        super().__init__()
        self._filament: FilamentData | None = None
        self.setFixedWidth(300)
        self.setStyleSheet("""
            FilamentForm {
                background: white;
                border-left: 0.5px solid #D3D1C7;
            }
        """)
 
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)
 
        self.form_title = QLabel("Novo filamento")
        self.form_title.setStyleSheet(
            "font-size: 15px; font-weight: 500; color: #2C2C2A;")
        root.addWidget(self.form_title)
        root.addWidget(make_divider())
 
        # tipo + marca
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        c1 = QVBoxLayout(); c1.setSpacing(4)
        c1.addWidget(form_label("Tipo"))
        self.tipo_combo = styled_combo(self.TIPOS)
        c1.addWidget(self.tipo_combo)
 
        c2 = QVBoxLayout(); c2.setSpacing(4)
        c2.addWidget(form_label("Marca"))
        self.marca_combo = styled_combo(self.MARCAS)
        c2.addWidget(self.marca_combo)
 
        row1.addLayout(c1)
        row1.addLayout(c2)
        root.addLayout(row1)
 
        # nome da cor
        root.addWidget(form_label("Nome da cor"))
        self.cor_input = styled_input("Ex: Azul royal")
        root.addWidget(self.cor_input)
 
        # cor hex (color picker)
        root.addWidget(form_label("Cor (hex)"))
        cor_row = QHBoxLayout()
        cor_row.setSpacing(8)
        self.cor_hex_input = styled_input("#000000")
        self.cor_preview = QFrame()
        self.cor_preview.setFixedSize(28, 28)
        self.cor_preview.setStyleSheet(
            "background: #000000; border-radius: 14px;"
            " border: 0.5px solid #D3D1C7;")
        self.pick_btn = QPushButton("⬛ Escolher")
        self.pick_btn.setFixedHeight(28)
        self.pick_btn.setStyleSheet("""
            QPushButton {
                border: 0.5px solid #B4B2A9; border-radius: 6px;
                padding: 0 10px; font-size: 11px;
                background: transparent; color: #2C2C2A;
            }
            QPushButton:hover { background: #F1EFE8; }
        """)
        self.pick_btn.clicked.connect(self._pick_color)
        self.cor_hex_input.textChanged.connect(self._on_hex_changed)
        cor_row.addWidget(self.cor_preview)
        cor_row.addWidget(self.cor_hex_input, stretch=1)
        cor_row.addWidget(self.pick_btn)
        root.addLayout(cor_row)
 
        # preço/kg
        root.addWidget(form_label("Preço/kg (R$)"))
        self.preco_input = styled_input("89,90")
        root.addWidget(self.preco_input)
 
        # peso bobina + peso usado
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        c3 = QVBoxLayout(); c3.setSpacing(4)
        c3.addWidget(form_label("Peso bobina (g)"))
        self.bobina_input = styled_input("1000")
        c3.addWidget(self.bobina_input)
 
        c4 = QVBoxLayout(); c4.setSpacing(4)
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
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                border: 0.5px solid #B4B2A9; border-radius: 6px;
                padding: 0 14px; font-size: 12px;
                background: transparent; color: #2C2C2A;
            }
            QPushButton:hover { background: #F1EFE8; }
        """)
        self.save_btn = QPushButton("Salvar")
        self.save_btn.setFixedHeight(32)
        self.save_btn.setStyleSheet("""
            QPushButton {
                border: none; border-radius: 6px;
                padding: 0 14px; font-size: 12px;
                background: #185FA5; color: white;
            }
            QPushButton:hover { background: #0C447C; }
        """)
        self.cancel_btn.clicked.connect(self.cancelled.emit)
        self.save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        root.addLayout(btn_row)
 
    def load(self, filament: FilamentData | None):
        """Popula o formulário. None = novo filamento."""
        self._filament = filament
        if filament is None:
            self.form_title.setText("Novo filamento")
            self.tipo_combo.setCurrentText("PLA")
            self.marca_combo.setCurrentText("Polymaker")
            self.cor_input.clear()
            self.cor_hex_input.setText("#000000")
            self.preco_input.setText("89,90")
            self.bobina_input.setText("1000")
            self.usado_input.setText("0")
        else:
            self.form_title.setText("Editar filamento")
            self.tipo_combo.setCurrentText(filament.tipo)
            self.marca_combo.setCurrentText(filament.marca)
            self.cor_input.setText(filament.cor)
            self.cor_hex_input.setText(filament.cor_str or "#000000")
            self.preco_input.setText(f"{filament.preco_kg:.2f}".replace(".", ","))
            self.bobina_input.setText(str(int(filament.peso_bobina_g)))
            self.usado_input.setText(str(int(filament.peso_usado_g)))
 
    def _pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.cor_hex_input.setText(color.name())
 
    def _on_hex_changed(self, text):
        if QColor(text).isValid():
            self.cor_preview.setStyleSheet(
                f"background: {text}; border-radius: 14px;"
                " border: 0.5px solid #D3D1C7;")
 
    def _on_save(self):
        try:
            preco  = float(self.preco_input.text().replace(",", "."))
            bobina = float(self.bobina_input.text().replace(",", "."))
            usado  = float(self.usado_input.text().replace(",", "."))
        except ValueError:
            StyledMessageBox.warning(
                self, "Valor inválido",
                "Preço, peso da bobina e peso usado devem ser numéricos.")
            return
 
        if self._filament is None:
            self._filament = FilamentData()
 
        self._filament.tipo          = self.tipo_combo.currentText()
        self._filament.marca         = self.marca_combo.currentText()
        self._filament.cor           = self.cor_input.text().strip() or "Sem nome"
        self._filament.cor_str       = self.cor_hex_input.text().strip()
        self._filament.preco_kg      = preco
        self._filament.peso_bobina_g = bobina
        self._filament.peso_usado_g  = usado
 
        self.saved.emit(self._filament)


class FilamentPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._filaments: list[FilamentData] = []
        self._cards: list[FilamentCard] = []
 
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
 
        # coluna esquerda — lista
        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(0)
 
        # topbar da página
        topbar = QWidget()
        topbar.setFixedHeight(56)
        topbar.setStyleSheet("border-bottom: 0.5px solid #D3D1C7; background: white;")
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(20, 0, 20, 0)
        title = QLabel("Filamentos")
        title.setStyleSheet("font-size: 15px; font-weight: 500; color: #2C2C2A;")
        self.add_btn = QPushButton("+ Novo filamento")
        self.add_btn.setFixedHeight(32)
        self.add_btn.setStyleSheet("""
            QPushButton {
                border: none; border-radius: 6px;
                padding: 0 16px; font-size: 12px;
                background: #185FA5; color: white;
            }
            QPushButton:hover { background: #0C447C; }
        """)
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
        self.list_layout.setContentsMargins(20, 16, 20, 16)
        self.list_layout.setSpacing(10)
        self.list_layout.addStretch()
 
        # estado vazio
        self.empty_lbl = QLabel("Nenhum filamento cadastrado.\nClique em \"+ Novo filamento\" para começar.")
        self.empty_lbl.setAlignment(Qt.AlignCenter)
        self.empty_lbl.setStyleSheet("font-size: 13px; color: #888780; padding: 40px;")
        self.list_layout.insertWidget(0, self.empty_lbl)
 
        scroll.setWidget(self.list_container)
        left.addWidget(scroll)
 
        left_widget = QWidget()
        left_widget.setLayout(left)
        root.addWidget(left_widget, stretch=1)
 
        # coluna direita — formulário (começa escondida)
        self.form = FilamentForm()
        self.form.hide()
        self.form.saved.connect(self._on_form_saved)
        self.form.cancelled.connect(self._close_form)
        root.addWidget(self.form)
 
    # ── lista ──
 
    def _rebuild_list(self, event=None):
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
        