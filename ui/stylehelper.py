from PySide6.QtWidgets import QComboBox, QFrame, QLabel, QLineEdit


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
