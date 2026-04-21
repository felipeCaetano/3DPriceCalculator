from typing import List

from PySide6.QtCore import QPropertyAnimation, QSize, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QColorDialog, QFrame, QHBoxLayout, QLabel, \
    QMdiSubWindow, QMessageBox, QProgressBar, QPushButton, QScrollArea, QStyle, \
    QStyleOption, QVBoxLayout, QWidget

from models.filament import FilamentData
from models.piece import PieceData
from ui.clicklable import ClickableLabel, ColoredDot
from ui.hamburgerbutton import HamburgerButton
from ui.styledmessagebox import StyledMessageBox
from ui.stylehelper import form_label, make_divider, panel_title, styled_combo, \
    styled_input


class TopBar(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setFixedHeight(48)
        self.setStyleSheet(
            "border-bottom: 0.5px solid #D3D1C7;")

        self.layout.setContentsMargins(64, 0, 16, 0)
        self.layout.setSpacing(8)
        self.setLayout(self.layout)
        self.title_lbl = QLabel(f'Nova Peça - precificação')
        self.title_lbl.setStyleSheet(
            "font-size: 15px; font-weight: 500; color: #FCFCFA;")
        self.layout.addWidget(self.title_lbl)
        self.layout.addStretch()
        self.cancel_btn = QPushButton('Cancelar')
        self.cancel_btn.setFixedHeight(30)
        self.cancel_btn.setStyleSheet("""
                    QPushButton {
                        border: 0.5px solid #B4B2A9;
                        border-radius: 6px;
                        padding: 0 14px;
                        font-size: 12px;
                        background: transparent;
                        color: #FCFCFA;
                    }
                    QPushButton:hover { background: #F12F28; color: #2C2C2A;}
                """)
        self.cancel_btn.clicked.connect(self.on_cancel)
        self.layout.addWidget(self.cancel_btn)
        self.save_btn = QPushButton('Salvar')
        self.save_btn.setFixedHeight(30)
        self.save_btn.setStyleSheet("""
                    QPushButton {
                        border: none;
                        border-radius: 6px;
                        padding: 0 14px;
                        font-size: 12px;
                        background: #185FA5;
                        color: white;
                    }
                    QPushButton:hover { background: #0C447C; }
                """)
        self.save_btn.clicked.connect(self.on_save)
        self.layout.addWidget(self.save_btn)

    def on_cancel(self):
        ...

    def on_save(self, value):
        ...

    def set_title(self, nome: str):
        """Atualiza o título da topbar com o nome da peça em tempo real."""
        text = f"{nome} — precificação" if nome else "Nova Peça — precificação"
        self.title_lbl.setText(text)


class MetricCard(QWidget):
    def __init__(self, label: str, color: str = "#2C2C2A"):
        super().__init__()
        self.setStyleSheet("background: #F1EFE8; border-radius: 8px;")
        self.setFixedHeight(64)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(4)

        self._label = QLabel(label)
        self._label.setStyleSheet(
            "font-size: 11px; color: #888780; background: transparent;")

        self._value = QLabel("R$ 0,00")
        self._value.setStyleSheet(
            f"font-size: 20px; font-weight: 500; color: {color};"
            " background: transparent;")

        layout.addWidget(self._label)
        layout.addWidget(self._value)

    def set_value(self, valor: float):
        """Recebe um float e exibe como moeda brasileira."""
        self._value.setText(
            f"R$ {valor:,.2f}".replace(",", "X")
            .replace(".", ",").replace("X",".")
        )

    def set_label(self, text: str):
        self._label.setText(text)


class MetricsRow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self.card_material =  MetricCard("Custo de material","#185FA5")
        layout.addWidget(self.card_material)
        self.card_energia = MetricCard("Custo de energia", "#854F0B")
        layout.addWidget(self.card_energia)
        self.card_total = MetricCard("Custo total", "#2C2C2A")
        layout.addWidget(self.card_total)
        self.card_venda = MetricCard("Preço sugerido", "#3B6D11")
        layout.addWidget(self.card_venda)

    def atualizar(self, piece: PieceData, filaments: List[FilamentData]):
        pg = 0
        for filament in filaments:
            pg += filament.preco_grama
        self.card_material.set_value(piece.custo_material(pg))
        self.card_energia.set_value(piece.custo_energia())
        self.card_total.set_value(piece.custo_total(pg))
        self.card_venda.set_value(piece.preco_venda(pg))


# ── painel genérico ───────────────────────────────────────────────────────────
class Panel(QWidget):
    def __init__(self, title_text, badge_text=None):
        super().__init__()
        self.setStyleSheet("""
            Panel {
                border: 0.5px solid #D3D1C7;
                border-radius: 12px;
                background: white;
            }
        """)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # header
        header = QWidget()
        header.setFixedHeight(38)
        header.setStyleSheet("background: transparent;")
        h = QHBoxLayout(header)
        h.setContentsMargins(14, 0, 14, 0)
        h.addWidget(panel_title(title_text))
        if badge_text:
            self._add_badge(badge_text, h)

        self._layout.addWidget(header)
        self._layout.addWidget(make_divider())

        # body
        self.body = QWidget()
        self.body.setStyleSheet("background: transparent;")
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(14, 12, 14, 12)
        self.body_layout.setSpacing(8)
        self._layout.addWidget(self.body)

    def _add_badge(self, text, h: QHBoxLayout):
        badge = QLabel(text)
        badge.setStyleSheet("""
            background: #E6F1FB; color: #185FA5;
            font-size: 10px; font-weight: 500;
            padding: 2px 10px; border-radius: 10px;
        """)
        h.addStretch()
        h.addWidget(badge)

    def add(self, widget):
        self.body_layout.addWidget(widget)

    def add_layout(self, layout):
        self.body_layout.addLayout(layout)

# ── painel esquerdo: dados da peça ───────────────────────────────────────────
class PiecePanel(Panel):
    def __init__(self, piece: PieceData):
        super().__init__("Dados da peça", badge_text="Em edição")
        self.piece = piece
        self.dot_count = 0

        # nome da peça (linha inteira)
        self.add(form_label("Nome da peça"))
        self.name_input = styled_input("Ex: Suporte de parede articulado")
        self.name_input.setText(piece.nome)
        self.add(self.name_input)

        # peso + tempo
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        col1 = QVBoxLayout()
        col1.setSpacing(4)
        col1.addWidget(form_label("Peso impresso (g)"))
        self.weight_input = styled_input("0")
        self.weight_input.setText(str(piece.peso_g) if piece.peso_g else "")
        col1.addWidget(self.weight_input)

        col2 = QVBoxLayout()
        col2.setSpacing(4)
        col2.addWidget(form_label("Tempo de impressão"))
        self.time_input = styled_input("Ex: 3h 20min")
        self.time_input.setText(
            str(piece.tempo_horas) if piece.tempo_horas else "")
        col2.addWidget(self.time_input)

        row1.addLayout(col1)
        row1.addLayout(col2)
        self.add_layout(row1)

        # infill + qualidade
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        col3 = QVBoxLayout()
        col3.setSpacing(4)
        col3.addWidget(form_label("Infill (%)"))
        self.infill_input = styled_input("20")
        self.infill_input.setText(str(piece.infill_pct))
        col3.addWidget(self.infill_input)

        col4 = QVBoxLayout()
        col4.setSpacing(4)
        col4.addWidget(form_label("Qualidade (mm)"))
        self.quality_combo = styled_combo(
            ["0.2 mm (normal)", "0.1 mm (fina)", "0.3 mm (rápida)"])
        col4.addWidget(self.quality_combo)

        row2.addLayout(col3)
        row2.addLayout(col4)
        self.add_layout(row2)

        # cores utilizadas
        self.add_dot = ClickableLabel("+")
        self.add_dot.setFixedSize(32, 32)
        self.add_dot.setAlignment(Qt.AlignCenter)
        self.add_dot.setStyleSheet(
            "border:0.5px dashed #B4B2A9;"
            " border-radius:9px; "
            "font-size:10px; "
            "color:#888780;")
        self.add_dot.clicked.connect(self._on_add_dot_clicked)

        self.add(form_label("Cores utilizadas"))
        self.colors_row1 = QHBoxLayout()
        self.colors_row1.setSpacing(8)
        self.colors_row1.addWidget(self.add_dot)
        self.colors_row1.addStretch()
        self.add_layout(self.colors_row1)

        self.colors_row2 = QHBoxLayout()
        self.colors_row2.setSpacing(8)
        self.colors_row2.addStretch()
        self.add_layout(self.colors_row2)
        for filament in self.piece.filamentos:
            self._insert_dot(filament.cor_str)
        self.add(make_divider())

        # observações
        self.add(form_label("Observações"))
        self.obs_input = styled_input("Ex: impressão pausada 1x — sem defeitos")
        self.obs_input.setText(piece.observacoes)
        self.add(self.obs_input)
        self.body_layout.addStretch()

    def _make_dot(self, color: str):
        dot = ColoredDot()
        dot.setFixedSize(32, 32)
        dot.handle_data(color)
        dot.clicked.connect(dot.handle_data)
        return dot

    def _insert_dot(self, color: str, sync_model: bool = False):
        """
        sync_model=False → apenas desenha o dot (usado na inicialização,
                            iterando sobre cores que já estão no modelo)
        sync_model=True  → desenha e também adiciona a cor ao modelo
                            (usado quando o usuário escolhe uma cor nova)
        """
        if self.dot_count >= 16:
            QMessageBox.warning(self, "Limite atingido",
                                "Número máximo de 16 cores alcançado!")
            return

        dot = self._make_dot(color)
        self.dot_count += 1

        if self.dot_count <= 8:
            idx = self.colors_row1.indexOf(self.add_dot)
            self.colors_row1.insertWidget(idx, dot)

            if self.dot_count == 8:
                self.colors_row1.removeWidget(self.add_dot)
                self.colors_row2.insertWidget(0, self.add_dot)
        else:
            idx = self.colors_row2.indexOf(self.add_dot)
            self.colors_row2.insertWidget(idx, dot)
        if sync_model:                          # só append quando vier do usuário
            self.piece.filamentos.append(FilamentData(cor_str=color))

    def _on_add_dot_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self._insert_dot(color.name(), sync_model=True)

    def collect(self) -> bool:
        """Valida e grava os campos no modelo. Retorna False se inválido."""
        nome = self.name_input.text().strip()
        if not nome:
            StyledMessageBox.warning(
                self,"Campo obrigatório",
                "<font color=black>Informe o nome da peça.</font>")
            return False
        try:
            peso = float(self.weight_input.text().replace(",", "."))
            tempo = self.get_prod_time_h(self.time_input.text())
            infill = int(self.infill_input.text())
        except ValueError:
            StyledMessageBox.warning(
                self,
                "Valor inválido",
                "<font color=black>"
                "Peso, tempo e infill devem ser numéricos."
                "</font>")
            return False

        self.piece.nome = nome
        self.piece.peso_g = peso
        self.piece.tempo_horas = tempo
        self.piece.infill_pct = infill
        self.piece.observacoes = self.obs_input.text()
        return True

    def get_prod_time_h(self, text: str) -> float:
        if not 'h' in text.lower() and len(text) > 2:
            StyledMessageBox.warning(
                self, "Formato Inválido",
                "<font color=black>Entre com o tempo no formato: xxhyy</font>") # NOQA
            return 0.0
        hora, minuto= text.lower().split('h')
        hora.strip()
        minuto = minuto[:2]
        tempo = float(hora) + float(minuto)/60
        return tempo


# ── painel direito superior: filamento ───────────────────────────────────────
class FilamentPanel(Panel):
    def __init__(self, filament: List[FilamentData]):
        super().__init__("Filamento")
        self.filament = filament

        row1 = QHBoxLayout()
        row1.setSpacing(8)
        col1 = QVBoxLayout()
        col1.setSpacing(4)
        col1.addWidget(form_label("Tipo"))
        self.type_combo = styled_combo(["PLA", "PETG", "ABS", "TPU", "ASA"])
        self.type_combo.setCurrentText(self.filament[0].tipo)
        col1.addWidget(self.type_combo)

        col2 = QVBoxLayout()
        col2.setSpacing(4)
        col2.addWidget(form_label("Marca"))
        self.brand_combo = styled_combo(
            [
                "Polymaker", "Bambu", "Hatchbox", "eSUN", "MultiLaser",
                "Creality"
            ])
        self.brand_combo.setCurrentText(self.filament[0].marca)
        col2.addWidget(self.brand_combo)

        row1.addLayout(col1)
        row1.addLayout(col2)
        self.add_layout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(8)

        col3 = QVBoxLayout()
        col3.setSpacing(4)
        col3.addWidget(form_label("Cor"))
        self.color_combo = styled_combo(
            ["Azul", "Vermelho", "Branco", "Preto"])
        self.color_combo.setCurrentText(self.filament[0].cor)
        col3.addWidget(self.color_combo)

        col4 = QVBoxLayout()
        col4.setSpacing(4)
        col4.addWidget(form_label("Preço/kg (R$)"))
        self.price_input = styled_input("89,90")
        self.price_input.setText(
            f"{self.filament[0].preco_kg:.2f}".replace(".", ",")
        )
        col4.addWidget(self.price_input)

        row2.addLayout(col3)
        row2.addLayout(col4)
        self.add_layout(row2)

        # barra de bobina
        spool_label_row = QHBoxLayout()
        spool_label_row.addWidget(form_label("Bobina restante"))
        pct = QLabel("62%")
        pct.setStyleSheet("font-size: 11px; color: #5F5E5A;")
        spool_label_row.addStretch()
        spool_label_row.addWidget(pct)
        self.add_layout(spool_label_row)

        bar = QProgressBar()
        bar.setValue(62)
        bar.setFixedHeight(6)
        bar.setTextVisible(False)
        bar.setStyleSheet(f"""
            QProgressBar {{ border-radius:3px; background:#D3D1C7; }}
            QProgressBar::chunk {{ border-radius:3px; 
            background:{self.filament[0].cor_str}; }}
        """)
        self.add(bar)

    def collect(self):
        """Valida e grava os campos no modelo. Retorna False se inválido."""
        try:
            preco = float(self.price_input.text().replace(",", "."))
        except ValueError:
            StyledMessageBox.warning(
                self,
                "Valor inválido",
                """<font color=black>
                            Preço do filamento deve ser numérico.
                    </font>"""
            )
            return False

        self.filament.tipo = self.type_combo.currentText()
        self.filament.marca = self.brand_combo.currentText()
        self.filament.cor = self.color_combo.currentText()
        self.filament.preco_kg = preco
        return True


# ── painel direito inferior: custos ──────────────────────────────────────────
class CostPanel(Panel):
    def __init__(self, piece: PieceData, filament: List[FilamentData]):
        super().__init__("Custos & precificação")
        self.piece = piece
        self.filament = filament

        def cost_row(label):
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("font-size: 12px; color: #5F5E5A;")
            val = QLabel("R$ 0,00")
            val.setStyleSheet(
                "font-size: 12px; font-weight: 500; color: #2C2C2A;")
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(val)
            return row, val

        r1, self.val_material = cost_row("Material")
        r2, self.val_energia  = cost_row("Energia")
        r3, self.val_mao_obra = cost_row("Mão de obra")
        self.add_layout(r1)
        self.add_layout(r2)
        self.add_layout(r3)
        self.add(make_divider())

        r4, self.val_total = cost_row("Custo total")
        self.add_layout(r4)

        margin_row = QHBoxLayout()
        margin_lbl = QLabel("Margem (%)")
        margin_lbl.setStyleSheet("font-size: 12px; color: #5F5E5A;")
        self.margin_input = styled_input("150")
        self.margin_input.setText(str(int(piece.margem_pct)))
        self.margin_input.setFixedWidth(70)
        self.margin_input.setAlignment(Qt.AlignRight)
        margin_row.addWidget(margin_lbl)
        margin_row.addStretch()
        margin_row.addWidget(self.margin_input)
        self.add_layout(margin_row)

        self.add(make_divider())

        final_row = QHBoxLayout()
        final_lbl = QLabel("Preço de venda")
        final_lbl.setStyleSheet(
            "font-size: 12px; font-weight: 500; color: #2C2C2A;")
        self.final_value = QLabel("R$ 0,00")
        self.final_value.setStyleSheet(
            "font-size: 14px; font-weight: 500; color: #185FA5;")
        final_row.addWidget(final_lbl)
        final_row.addStretch()
        final_row.addWidget(self.final_value)
        self.add_layout(final_row)

    @staticmethod
    def _fmt(v: float) -> str:
        return (f"R$ {v:,.2f}"
                .replace(",", "X").replace(".", ",").replace("X", "."))

    def atualizar(self):
        """Recalcula todos os valores com os dados atuais dos modelos."""
        try:
            self.piece.margem_pct = float(
                self.margin_input.text().replace(",", ".") or "0")
        except ValueError:
            StyledMessageBox.warning(
                self, "Erro de margem", "A margem deve ser numérica!"
            )
        print(self.filament)
        pg  = sum([x.preco_grama for x in self.filament])
        mat = self.piece.custo_material(pg)
        ene = self.piece.custo_energia()
        mo  = self.piece.mao_de_obra
        tot = self.piece.custo_total(pg)
        vnd = self.piece.preco_venda(pg)

        self.val_material.setText(self._fmt(mat))
        self.val_energia.setText(self._fmt(ene))
        self.val_mao_obra.setText(self._fmt(mo))
        self.val_total.setText(self._fmt(tot))
        self.final_value.setText(self._fmt(vnd))


# ── área principal de conteúdo
class MainContent(QWidget):
    def __init__(self, piece, filament: List[FilamentData]):
        super().__init__()
        self.piece = piece
        self.filament = filament
        self.setStyleSheet("background: #F5F4F0;")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 8, 16, 8)
        outer.setSpacing(16)

        self.metrics = MetricsRow()
        outer.addWidget(self.metrics)

        panels_row = QHBoxLayout()
        panels_row.setSpacing(8)

        self.piece_panel = PiecePanel(piece)
        self.filament_panel = FilamentPanel(filament)
        self.cost_panel = CostPanel(piece, filament)

        panels_row.addWidget(self.piece_panel, stretch=1)

        right_col = QVBoxLayout()
        right_col.setSpacing(14)
        right_col.addWidget(self.filament_panel)
        right_col.addWidget(self.cost_panel)
        panels_row.addLayout(right_col, stretch=1)

        outer.addLayout(panels_row)

        self._conectar_signals()
        self.recalcular()

    def _conectar_signals(self):
        """Qualquer alteração nos campos numéricos dispara o recálculo."""
        for w in (self.piece_panel.weight_input,
                  self.piece_panel.time_input,
                  self.piece_panel.infill_input,
                  self.filament_panel.price_input,
                  self.cost_panel.margin_input):
            w.textChanged.connect(self._on_input_changed)

        self.piece_panel.name_input.textChanged.connect(self._on_name_changed)

    def _on_input_changed(self):
        """Atualiza o modelo silenciosamente e recalcula."""
        try:
            self.piece.peso_g = float(
                self.piece_panel.weight_input.text().replace(",", ".") or "0")
            self.piece.tempo_horas = self.piece_panel.get_prod_time_h(
                self.piece_panel.time_input.text().replace(",", ".") or "0")
            for filament in self.filament:
                filament.preco_kg = float(
                self.filament_panel.price_input.text().replace(",", ".") or "0")
        except ValueError:
            ...
        self.recalcular()

    def _on_name_changed(self, text):
        self.piece.nome = text
        # sobe na hierarquia para atualizar o título da topbar
        try:
            widget_content = self.parent().parent().parent()
            if hasattr(widget_content, "topbar"):
                widget_content.topbar.set_title(text)
        except AttributeError:
            pass

    def recalcular(self):
        self.metrics.atualizar(self.piece, self.filament)
        self.cost_panel.atualizar()


class WidgetContent(QWidget):
    def __init__(self, mdi):
        super(WidgetContent, self).__init__()
        self.mdi = mdi

        # piece, filament = db.load_piece(id)
        self.piece = PieceData(filamentos=[FilamentData(cor_str="#1565C0")])
        self.filament = self.piece.filamentos
        print(self.filament)
        #self.filament = FilamentData()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 0, 8, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.topbar = TopBar()
        self.topbar.save_btn.clicked.connect(self._on_save)
        self.topbar.cancel_btn.clicked.connect(self._on_cancel)
        self.layout.addWidget(self.topbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: #F5F4F0;")

        self.main_content = MainContent(self.piece, self.filament)
        scroll.setWidget(self.main_content)
        self.layout.addWidget(scroll)

        self.menu_btn = HamburgerButton(self)
        self.menu_btn.move(8, 8)  # canto superior esquerdo
        self.menu_btn.clicked.connect(self.show_menu)
        self.menu_btn.raise_()

    def _on_save(self):
        pc = self.main_content.piece_panel
        fc = self.main_content.filament_panel
        if pc.collect() and fc.collect():
            self.main_content.recalcular()
            # db.save_piece(self.piece, self.filament)
            QMessageBox.information(
                self, "Salvo",
                f"Peça '{self.piece.nome}' salva com sucesso!")

    def _on_cancel(self):
        reply = QMessageBox.question(
            self, "Cancelar", "Deseja descartar as alterações?",
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            pass  # reiniciar formulário ou fechar aba

    def show_menu(self):
        self.animation = QPropertyAnimation(self.mdi.menu, b"size")
        self.animation.setDuration(150)
        if self.menu_btn.isChecked():
            self.animation.setStartValue(QSize(0, self.mdi.height()))
            self.animation.setEndValue(QSize(270, self.mdi.height()))
        else:
            self.animation.setStartValue(QSize(270, self.mdi.height()))
            self.animation.setEndValue(QSize(0, self.mdi.height()))

        self.animation.valueChanged.connect(self._move_btn)
        self.animation.start()
        if self.menu_btn.isChecked():
            self.mdi.overlay.show()
            self.mdi.menu.show()
            self.mdi.setActiveSubWindow(self.mdi.overlay)
            self.mdi.setActiveSubWindow(self.mdi.menu)
        else:
            self.animation.finished.connect(self._close_menu)

    def _move_btn(self, value):
        self.menu_btn.move(value.width() + 8, 8)
        self.menu_btn.raise_()

    def _close_menu(self):
        self.mdi.overlay.hide()
        self.mdi.menu.hide()
        self.menu_btn.move(8, 8)
        self.menu_btn.raise_()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)


class Content(QMdiSubWindow):
    def __init__(self, parent):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.widget = WidgetContent(parent)
        self.setWidget(self.widget)
