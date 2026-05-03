from PySide6.QtWidgets import QComboBox, QFrame, QLabel, QLineEdit


# Estilização Global (QSS)
STYLE_SHEET = """
QMainWindow {
    background-color: #F8F9FA;
}

#Sidebar {
    background-color: #F0F2F5;
    border-right: 1px solid #E0E0E0;
    min-width: 200px;
}

#FilamentTopBar{
}

#FilamentForm {
    background: white;
    border-left: 0.5px solid #D3D1C7;
}

#ContentArea {
    background-color: #FFFFFF;
}

.Card {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 12px;
}

.SummaryCard {
    background-color: #FDFDFD;
    border: 1px solid #EAEAEA;
    border-radius: 10px;
    padding: 10px;
}
QDateEdit {
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 4px;
                background-color: white;
            }
QDateEdit::drop-down {border: none;
            }
QLabel{
    font-size: 11px; color: #5F5E5A;
    }
QLabel#MenuTitle {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-bottom: 5px;
}

QLabel#MenuSubtitle {
    font-size: 12px;
    color: #777;
    margin-bottom: 20px;
}

QPushButton#MenuButton {
    text-align: left;
    padding: 10px;
    border: none;
    border-radius: 5px;
    color: #555;
    font-weight: 500;
}

QPushButton#MenuButton:hover {
    background-color: #E8EBF0;
}

QPushButton#MenuButton[active="true"] {
    background-color: #DBEAFE;
    color: #2563EB;
}

QPushButton#FilamentCancelButton {
    border: 0.5px solid #B4B2A9; border-radius: 6px;
    padding: 0 14px; font-size: 12px;
    background: transparent; color: #2C2C2A;
}

QPushButton#FilamentCancelButton:hover { background: #F12F28; color: white }

QPushButton#FilamentSaveButton {
    border: none; border-radius: 6px;
    padding: 0 14px; font-size: 12px;
    background: #185FA5; color: white;
}

QPushButton#FilamentSaveButton:hover { background: #0C447C; }

QPushButton#FilamentNew {
    background: #185FA5;
    color: white;
    border-radius: 6px;
    padding: 0px 14px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton#FilamentNew:hover { background: #0C447C; }

QLabel#CardTitle {
    font-weight: bold;
    font-size: 14px;
    color: #333;
}

QLineEdit, QTextEdit {
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    padding: 8px;
    background-color: white;
    background: white;
    color: #2C2C2A;
}

QPushButton#PrimaryButton {
    background-color: #FFFFFF;
    border: 0.5px solid #B4B2A9;
    border-radius: 6px;
    padding: 0px 14px;
    font-size: 14px;
    font-weight: bold;
    background: transparent;
    color: #2C2C2A;
}

QPushButton#PrimaryButton:hover {
    background-color: #F3F4F6;
    color: #FCFCFA;
}

QSpinBox {
    border: 0.5px solid #B4B2A9;
    border-radius: 6px;
    padding: 0 8px;
    font-size: 12px;
    background: white;
    color: #2C2C2A;
}
QSpinBox:focus { border-color: #185FA5; }
QSpinBox:up-button { subcontrol-origin border; width: 18px; }
QSpinBox:down-button { subcontrol-origin border; width: 18px; }
"""

def make_divider():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("color: #D3D1C7;")
    line.setFixedHeight(1)
    return line


def make_section_label(text):
    label = QLabel(text.upper())
    label.setStyleSheet("""
        color: #888780;
        font-size: 10px;
        letter-spacing: 1px;
        padding: 12px 16px 4px 16px;
    """)
    label.setFixedHeight(30)
    return label


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
        QComboBox QAbstractItemView {
            border: 1px solid darkgray;
            selection-background-color: lightgray;
            background-color: white;
        }
    """)
    return w


def form_label(text):
    lbl = QLabel(text)
    lbl.setStyleSheet("font-size: 14px; color: #5F5E5A; font-weight: 700;")
    return lbl


def panel_title(text):
    lbl = QLabel(text)
    lbl.setStyleSheet("font-size: 13px; font-weight: 500; color: #2C2C2A;")
    return lbl
