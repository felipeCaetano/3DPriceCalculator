from PySide6.QtCore import Qt, QPropertyAnimation, QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QMdiSubWindow, QWidget, QHBoxLayout, QPushButton, \
    QStyleOption, QStyle, QLabel, QVBoxLayout, QScrollArea, QFrame, QLineEdit, \
    QComboBox, QProgressBar

from ui.clicklable import ColoredDot, ClickableLabel
from ui.hamburgerbutton import HamburgerButton


# ── helpers de estilo ────────────────────────────────────────────────────────

def make_divider():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("color: #D3D1C7;")
    line.setFixedHeight(1)
    return line


def styled_input(placeholder=""):
    w = QLineEdit()
    w.setPlaceholderText(placeholder)
    w.setFixedHeight(28)
    w.setStyleSheet("""
        QLineEdit {
            border: 0.5px solid #B4B2A9;
            border-radius: 6px;
            padding: 0 8px;
            font-size: 12px;
            background: white;
            color: #2C2C2A;
        }
        QLineEdit:focus { border-color: #185FA5; }
    """)
    return w


def styled_combo(options):
    w = QComboBox()
    for o in options:
        w.addItem(o)
    w.setFixedHeight(28)
    w.setStyleSheet("""
        QComboBox {
            border: 0.5px solid #B4B2A9;
            border-radius: 6px;
            padding: 0 8px;
            font-size: 12px;
            background: white;
            color: #2C2C2A;
        }
        QComboBox:focus { border-color: #185FA5; }
        QComboBox::drop-down { border: none; width: 20px; }
    """)
    return w


def form_label(text):
    lbl = QLabel(text)
    lbl.setStyleSheet("font-size: 11px; color: #5F5E5A;")
    return lbl


def panel_title(text):
    lbl = QLabel(text)
    lbl.setStyleSheet("font-size: 13px; font-weight: 500; color: #2C2C2A;")
    return lbl


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
        self.title = QLabel(f'Nova Peça - precificação')
        self.title.setStyleSheet(
            "font-size: 15px; font-weight: 500; color: #FCFCFA;")
        self.layout.addWidget(self.title)
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
        self.layout.addWidget(self.save_btn)


class MetricCard(QWidget):
    def __init__(self, label, value, color="#2C2C2A"):
        super().__init__()
        self.setStyleSheet("background: #F1EFE8; border-radius: 8px;")
        self.setFixedHeight(64)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(4)

        lbl = QLabel(label)
        lbl.setStyleSheet(
            "font-size: 11px; color: #888780; background: transparent;"
        )

        val = QLabel(value)
        val.setStyleSheet(
            f"font-size: 20px;"
            f"font-weight: 500;"
            f" color: {color}; "
            f"background: transparent;"
        )

        layout.addWidget(lbl)
        layout.addWidget(val)


class MetricsRow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self.filament_cost =  MetricCard(
            "Custo de material", "R$ 4,32", "#185FA5"
        )
        layout.addWidget(self.filament_cost)
        self.energy_cost = MetricCard(
            "Custo de energia", "R$ 1,17", "#854F0B"
        )
        layout.addWidget(self.energy_cost)
        self.total_cost = MetricCard(
            "Custo total", "R$ 7,49", "#2C2C2A"
        )
        layout.addWidget(self.total_cost)
        self.final_price = MetricCard(
            "Preço sugerido", "R$ 18,72", "#3B6D11"
        )
        layout.addWidget(self.final_price)


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
            self.set_badgetext(badge_text, h)

        self._layout.addWidget(header)
        self._layout.addWidget(make_divider())

        # body
        self.body = QWidget()
        self.body.setStyleSheet("background: transparent;")
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(14, 12, 14, 12)
        self.body_layout.setSpacing(8)
        self._layout.addWidget(self.body)

    def set_badgetext(self, badge_text, h: QHBoxLayout):
        badge = QLabel(badge_text)
        background_color = "#E6F1FB"
        color = "#185FA5"
        if badge_text == "Em edição":
            background_color = "#E6F1FB"
            color = "#185FA5"
        badge.setStyleSheet(f"""
                background: {background_color};
                color: {color};
                font-size: 10px;
                font-weight: 500;
                padding: 2px 10px;
                border-radius: 10px;
            """)
        h.addStretch()
        h.addWidget(badge)

    def add(self, widget):
        self.body_layout.addWidget(widget)

    def add_layout(self, layout):
        self.body_layout.addLayout(layout)

# ── painel esquerdo: dados da peça ───────────────────────────────────────────

class PiecePanel(Panel):
    def __init__(self):
        super().__init__("Dados da peça", badge_text="Em edição")

        # nome da peça (linha inteira)
        self.add(form_label("Nome da peça"))
        self.name_input = styled_input("Ex: Suporte de parede articulado")
        self.add(self.name_input)

        # peso + tempo
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        col1 = QVBoxLayout()
        col1.setSpacing(4)
        col1.addWidget(form_label("Peso impresso (g)"))
        self.weight_input = styled_input("0")
        col1.addWidget(self.weight_input)

        col2 = QVBoxLayout()
        col2.setSpacing(4)
        col2.addWidget(form_label("Tempo de impressão"))
        self.time_input = styled_input("Ex: 3h 20min")
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
        self.add(form_label("Cores utilizadas"))
        colors_row = QHBoxLayout()
        colors_row.setSpacing(8)
        for color in ["#1565C0", "#E53935", "#F5F5F5"]:
            dot = ColoredDot()
            dot.setFixedSize(32, 32)
            dot.setStyleSheet(
                f"background:{color};"
                f" border-radius:9px; "
                f"border:0.5px solid #D3D1C7;")
            dot.clicked.connect(dot.handle_data)
            colors_row.addWidget(dot)
        add_dot = ClickableLabel("+")
        add_dot.setFixedSize(32, 32)
        add_dot.setAlignment(Qt.AlignCenter)
        add_dot.setStyleSheet(
            "border:0.5px dashed #B4B2A9;"
            " border-radius:9px; "
            "font-size:10px; "
            "color:#888780;")
        add_dot.clicked.connect(lambda : print())
        colors_row.addWidget(add_dot)
        colors_row.addStretch()
        self.add_layout(colors_row)

        self.add(make_divider())

        # observações
        self.add(form_label("Observações"))
        self.obs_input = styled_input("Ex: impressão pausada 1x — sem defeitos")
        self.add(self.obs_input)
        self.badge_text = "Salvo"
        self.body_layout.addStretch()


# ── painel direito superior: filamento ───────────────────────────────────────

class FilamentPanel(Panel):
    def __init__(self):
        super().__init__("Filamento")

        row1 = QHBoxLayout()
        row1.setSpacing(8)

        col1 = QVBoxLayout()
        col1.setSpacing(4)
        col1.addWidget(form_label("Tipo"))
        self.type_combo = styled_combo(["PLA", "PETG", "ABS", "TPU", "ASA"])
        col1.addWidget(self.type_combo)

        col2 = QVBoxLayout()
        col2.setSpacing(4)
        col2.addWidget(form_label("Marca"))
        self.brand_combo = styled_combo(
            ["Polymaker", "Bambu", "Hatchbox", "eSUN"])
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
            ["Azul royal", "Vermelho", "Branco", "Preto"])
        col3.addWidget(self.color_combo)

        col4 = QVBoxLayout()
        col4.setSpacing(4)
        col4.addWidget(form_label("Preço/kg (R$)"))
        self.price_input = styled_input("89,90")
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
        bar.setStyleSheet("""
            QProgressBar { border-radius:3px; background:#D3D1C7; }
            QProgressBar::chunk { border-radius:3px; background:#185FA5; }
        """)
        self.add(bar)


# ── painel direito inferior: custos ──────────────────────────────────────────

class CostPanel(Panel):
    def __init__(self):
        super().__init__("Custos & precificação")

        def cost_row(label, value, value_color="#2C2C2A"):
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("font-size: 12px; color: #5F5E5A;")
            val = QLabel(value)
            val.setStyleSheet(
                f"font-size: 12px; font-weight: 500; color: {value_color};")
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(val)
            return row

        self.add_layout(cost_row("Material (48g × R$0,09/g)", "R$ 4,32"))
        self.add_layout(cost_row("Energia (3.3h × 0.3kW × R$1,18)", "R$ 1,17"))
        self.add_layout(cost_row("Mão de obra", "R$ 2,00"))
        self.add(make_divider())
        self.add_layout(cost_row("Custo total", "R$ 7,49"))

        # margem editável
        margin_row = QHBoxLayout()
        margin_lbl = QLabel("Margem")
        margin_lbl.setStyleSheet("font-size: 12px; color: #5F5E5A;")
        self.margin_input = styled_input("150%")
        self.margin_input.setFixedWidth(70)
        self.margin_input.setAlignment(Qt.AlignRight)
        margin_row.addWidget(margin_lbl)
        margin_row.addStretch()
        margin_row.addWidget(self.margin_input)
        self.add_layout(margin_row)

        self.add(make_divider())

        # preço final
        final_row = QHBoxLayout()
        final_lbl = QLabel("Preço de venda")
        final_lbl.setStyleSheet(
            "font-size: 12px; font-weight: 500; color: #2C2C2A;")
        self.final_value = QLabel("R$ 18,72")
        self.final_value.setStyleSheet(
            "font-size: 14px; font-weight: 500; color: #185FA5;")
        final_row.addWidget(final_lbl)
        final_row.addStretch()
        final_row.addWidget(self.final_value)
        self.add_layout(final_row)


# ── área principal de conteúdo
class MainContent(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #F5F4F0;")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 8, 16, 8)
        outer.setSpacing(16)

        # cards de métricas
        outer.addWidget(MetricsRow())

        # painéis lado a lado
        panels_row = QHBoxLayout()
        panels_row.setSpacing(8)

        # esquerda
        self.piece_panel = PiecePanel()
        panels_row.addWidget(self.piece_panel, stretch=1)

        # direita — dois painéis empilhados
        right_col = QVBoxLayout()
        right_col.setSpacing(14)
        self.filament_panel = FilamentPanel()
        self.cost_panel = CostPanel()
        right_col.addWidget(self.filament_panel)
        right_col.addWidget(self.cost_panel)

        panels_row.addLayout(right_col, stretch=1)
        outer.addLayout(panels_row)


class WidgetContent(QWidget):
    def __init__(self, mdi):
        super(WidgetContent, self).__init__()
        self.mdi = mdi
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.topbar = TopBar()
        self.layout.addWidget(self.topbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: #F5F4F0;")
        self.main_content = MainContent()
        scroll.setWidget(self.main_content)
        self.layout.addWidget(scroll)

        self.menu_btn = HamburgerButton(self)
        self.menu_btn.move(8, 8)  # canto superior esquerdo

        self.menu_btn.clicked.connect(self.show_menu)

        self.menu_btn.raise_()

    def show_menu(self):
        self.animation = QPropertyAnimation(self.mdi.menu, b"size")
        self.animation.setDuration(150)
        if self.menu_btn.isChecked():
            self.animation.setStartValue(QSize(0, self.mdi.height()))
            self.animation.setEndValue(QSize(270, self.mdi.height()))
        else:
            # fechando
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
        self.menu_btn.move(value.width() + 8, 8)  # canto superior esquerdo
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
        super(Content, self).__init__()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.widget = WidgetContent(parent)
        self.setWidget(self.widget)