from PySide6.QtWidgets import QComboBox, QFrame, QLabel, QLineEdit, QSizePolicy
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt

# ─── Paleta ────────────────────────────────────────────────────────────────
C_BG = "#f5f3ef"   # fundo geral (bege quente)
C_SURFACE = "#ffffff"   # cards / tabelas
C_BORDER = "#e0dbd0"   # borda suave
C_BORDER2 = "#d0cac0"   # borda inputs (bege)
C_TEXT = "#1c1917"   # texto principal
C_TEXT2 = "#44403c"   # texto secundário
C_TEXT3 = "#78716c"   # texto terciário / labels
C_TEXT4 = "#a8a29e"   # texto muito suave

C_BLUE = "#2563eb"   # azul primário
C_BLUE_LIGHT = "#dbeafe"   # azul claro (badge / focus)
C_BLUE_TEXT = "#1d4ed8"   # texto azul

C_GREEN = "#16a34a"  # verde
C_GREEN_LIGHT = "#dcfce7"  # verde claro
C_GREEN_TEXT = "#15803d"  # texto verde

C_ORANGE = "#d97706"  # laranja (aviso)
C_ORANGE_LIGHT = "#fef9c3"
C_ORANGE_TEXT = "#854d0e"

C_RED = "#dc2626"  # vermelho


STYLE_SHEET = f"""
/* ── Base ─────────────────────────────────────── */
QWidget {{
    background-color: {C_BG};
    font-family: -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
    color: {C_TEXT};
}}

/* ── Cards ────────────────────────────────────── */
QWidget[class="Card"] {{
    background-color: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-radius: 10px;
    padding: 14px;
}}

/* ── Labels ───────────────────────────────────── */
QLabel#AppTitle {{
    font-size: 25px;
    font-weight: 900;
    color: {C_TEXT};
    background: transparent;
}}
QLabel#MenuTitle {{
    font-size: 20px;
    font-weight: 700;
    color: {C_TEXT};
    background: transparent;
}}
QLabel#CardTitle {{
    font-size: 16px;
    font-weight: 700;
    color: {C_TEXT};
    background: transparent;
}}
QLabel#MenuSubtitle {{
    font-size: 16px;
    color: {C_TEXT3};
    background: transparent;
}}
QLabel#SectionLabel {{
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: {C_TEXT3};
    background: transparent;
}}
QLabel#FormLabel {{
    font-size: 14px;
    color: {C_TEXT3};
    background: transparent;
}}
QLabel#PanelTitle {{
    font-size: 14px;
    font-weight: 600;
    color: {C_TEXT2};
    background: transparent;
}}
QLabel#FooterLabel {{
    font-size: 12px;
    color: {C_TEXT4};
    background: transparent;
}}
QLabel#HighlightValue {{
    font-size: 24px;
    font-weight: 700;
    color: {C_GREEN};
    background: transparent;
}}
QLabel#InfoBanner {{
    font-size: 14px;
    color: {C_BLUE_TEXT};
    background-color: #eff6ff;
    border: 1px solid {C_BLUE_LIGHT};
    border-radius: 8px;
    padding: 8px 12px;
}}
QLabel#SuccessBanner {{
    font-size: 14px;
    color: {C_GREEN_TEXT};
    background-color: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 8px;
    padding: 8px 12px;
}}
QLabel {{
    font-size: 12px;
    color: {C_TEXT};
    background: transparent;
}}

/* ── Botões ───────────────────────────────────── */
QPushButton {{
    font-family: -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 500;
}}
QPushButton#PrimaryButton {{
    background-color: {C_BLUE};
    color: white;
    border: none;
}}
QPushButton#PrimaryButton:hover {{
    background-color: {C_BLUE_TEXT};
}}
QPushButton#PrimaryButton:pressed {{
    background-color: #1e40af;
}}
QPushButton#GhostButton {{
    background-color: {C_SURFACE};
    color: {C_TEXT2};
    border: 1px solid {C_BORDER2};
}}
QPushButton#GhostButton:hover {{
    background-color: #f5f3ee;
}}
QPushButton#AddBtn {{
    background-color: {C_BLUE};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
}}
QPushButton#AddBtn:hover {{
    background-color: {C_BLUE_TEXT};
}}
QPushButton#SmallAddBtn {{
    background-color: {C_BLUE};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 500;
}}

/* ── QTabWidget ───────────────────────────────── */
QTabWidget::pane {{
    border: none;
    background: transparent;
    margin-top: 0px;
}}
QTabWidget {{
    background: transparent;
}}
QTabBar {{
    background: transparent;
}}
QTabBar::tab {{
    background: transparent;
    color: {C_TEXT3};
    font-size: 12px;
    font-weight: 400;
    padding: 8px 16px;
    border: none;
    border-bottom: 2px solid transparent;
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    color: {C_BLUE};
    border-bottom: 2px solid {C_BLUE};
    font-weight: 600;
    background: transparent;
}}
QTabBar::tab:hover:!selected {{
    color: {C_TEXT};
    background: transparent;
}}

/* ── QTableWidget ─────────────────────────────── */
QTableWidget {{
    background-color: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-radius: 10px;
    gridline-color: #f0ede8;
    selection-background-color: {C_BLUE_LIGHT};
    selection-color: {C_TEXT};
    font-size: 12px;
    alternate-background-color: #faf9f6;
}}
QTableWidget::item {{
    padding: 8px 10px;
    border-bottom: 1px solid #f0ede8;
}}
QTableWidget::item:selected {{
    background-color: {C_BLUE_LIGHT};
    color: {C_TEXT};
}}
QHeaderView {{
    background-color: #f5f3ee;
    border: none;
}}
QHeaderView::section {{
    background-color: #f5f3ee;
    color: {C_TEXT3};
    font-weight: 500;
    font-size: 11px;
    padding: 8px 10px;
    border: none;
    border-bottom: 1px solid {C_BORDER};
}}
QHeaderView::section:first {{
    border-top-left-radius: 10px;
}}
QHeaderView::section:last {{
    border-top-right-radius: 10px;
}}

/* ── QLineEdit ────────────────────────────────── */
QLineEdit {{
    background-color: {C_SURFACE};
    border: 1px solid {C_BORDER2};
    border-radius: 8px;
    padding: 7px 10px;
    font-size: 13px;
    color: {C_TEXT};
    selection-background-color: {C_BLUE_LIGHT};
}}
QLineEdit:focus {{
    border: 1px solid #93c5fd;
    outline: none;
}}
QLineEdit:disabled {{
    background-color: #f5f3ee;
    color: {C_TEXT4};
}}

/* ── QComboBox ────────────────────────────────── */
QComboBox {{
    background-color: {C_SURFACE};
    border: 1px solid {C_BORDER2};
    border-radius: 8px;
    padding: 7px 10px;
    font-size: 13px;
    color: {C_TEXT};
    selection-background-color: {C_BLUE_LIGHT};
}}
QComboBox:focus {{
    border: 1px solid #93c5fd;
}}
QComboBox::drop-down {{
    border: none;
    width: 22px;
}}
QComboBox::down-arrow {{
    width: 10px;
    height: 10px;
}}
QComboBox QAbstractItemView {{
    background-color: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-radius: 8px;
    selection-background-color: {C_BLUE_LIGHT};
    color: {C_TEXT};
    font-size: 13px;
    padding: 4px;
}}

/* ── QScrollBar ───────────────────────────────── */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {C_BORDER2};
    border-radius: 4px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: {C_BORDER2};
    border-radius: 4px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* ── QFrame (divider) ─────────────────────────── */
QFrame#Divider {{
    background-color: {C_BORDER};
    max-height: 1px;
    border: none;
}}
"""


# ─── Helper widgets ─────────────────────────────────────────────────────────

def form_label(text: str) -> QLabel:
    """Label pequeno para campo de formulário."""
    lbl = QLabel(text)
    lbl.setObjectName("FormLabel")
    return lbl


def panel_title(text: str) -> QLabel:
    """Título de painel / seção de card."""
    lbl = QLabel(text)
    lbl.setObjectName("PanelTitle")
    return lbl


def make_section_label(text: str) -> QLabel:
    """Label de seção com fundo de banner (info)."""
    lbl = QLabel(text)
    lbl.setObjectName("InfoBanner")
    lbl.setWordWrap(True)
    return lbl


def make_success_banner(text: str) -> QLabel:
    """Label de sucesso/resultado calculado."""
    lbl = QLabel(text)
    lbl.setObjectName("SuccessBanner")
    lbl.setWordWrap(True)
    return lbl


def make_divider() -> QFrame:
    """Linha divisória horizontal."""
    line = QFrame()
    line.setObjectName("Divider")
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Plain)
    line.setFixedHeight(1)
    return line


def styled_input(placeholder: str = "", value: str = "") -> QLineEdit:
    """QLineEdit estilizado."""
    inp = QLineEdit()
    if placeholder:
        inp.setPlaceholderText(placeholder)
    if value:
        inp.setText(value)
    return inp


def styled_combo(items: list[str], current: int = 0) -> QComboBox:
    """QComboBox estilizado."""
    cb = QComboBox()
    cb.addItems(items)
    cb.setCurrentIndex(current)
    return cb


def badge_color(status: str) -> tuple[QColor, QColor]:
    """Retorna (background, foreground) para um status badge."""
    s = status.lower()
    if "ativa" in s and "in" not in s:
        return QColor("#dcfce7"), QColor("#15803d")
    if "inativa" in s:
        return QColor("#fef9c3"), QColor("#854d0e")
    return QColor("#f5f3ee"), QColor("#44403c")