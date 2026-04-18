import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, 
                             QComboBox, QProgressBar, QTextEdit, QGridLayout, QGraphicsDropShadowEffect, QScrollArea)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QColor


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

QLabel#CardTitle {
    font-weight: bold;
    font-size: 14px;
    color: #333;
}

QLineEdit, QComboBox, QTextEdit {
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    padding: 8px;
    background-color: white;
}

QPushButton#PrimaryButton {
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: bold;
    background: transparent;
}

QPushButton#PrimaryButton:hover {
    background-color: #F3F4F6;
}
"""

class CostCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "Card")
        cost_lay = QVBoxLayout(self)
        cost_lay.addWidget(QLabel("Custos & precificação", objectName="CardTitle"))
        self.material_lbl = QLabel()
        self.energy_lbl = QLabel()
        self.work_lbl = QLabel()
        self.adtives_lbl = QLabel()
        self.embalagem_lbl = QLabel()
        self.labels_map = {
            "Material": self.material_lbl,
            "Energia": self.energy_lbl,
            "Mão de Obra": self.work_lbl,
            "Adicionais": self.adtives_lbl,
            "Embalagem": self.embalagem_lbl
        }
        
        details = [
            ("Material", "R$ 4,32"),
            ("Energia", "R$ 1,17"),
            ("Mão de Obra", "R$ 2,00"),
            ("Adicionais", "R$ 2,00"),
            ("Embalagem", "R$ 2,00")
        ]
        for desc, val in details:
            d_lay = QHBoxLayout()
            d_lay.addWidget(QLabel(desc))
            d_lay.addStretch()
            
            # Busca o label correto no dicionário
            target_label = self.labels_map.get(desc)
            if target_label:
                target_label.setText(val)
                d_lay.addWidget(target_label)
            cost_lay.addLayout(d_lay)

        cost_lay.addSpacing(4)
        cost_lay.addWidget(make_divider())
        total_lay = QHBoxLayout()
        total_lbl = QLabel("Custo total")
        total_lbl.setStyleSheet("font-weight: bold;")
        total_val = QLabel("R$ 7,49")
        total_val.setStyleSheet("font-weight: bold;")
        total_lay.addWidget(total_lbl); total_lay.addStretch(); total_lay.addWidget(total_val)
        cost_lay.addLayout(total_lay)

def make_divider():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("color: #D3D1C7;")
    line.setFixedHeight(1)
    return line

class FilamentCard(QFrame):
    """Card Filamento"""
    def __init__(self):
        super().__init__()
        self.setProperty("class", "Card")
        fil_lay = QVBoxLayout(self)
        fil_lay.addWidget(QLabel("Filamento", objectName="CardTitle"))
        
        f_grid = QGridLayout()
        f_grid.addWidget(QLabel("Tipo"), 0, 0)
        self.filament_type = QComboBox()
        for f_type in sorted(["PLA", "PETG", "ABS", "TPU", "ASA", "Nylon"]):
            self.filament_type.addItem(f_type)
        f_grid.addWidget(self.filament_type, 1, 0)
        f_grid.addWidget(QLabel("Marca"), 0, 1)
        self.filament_brand = QComboBox()
        for f_brand in sorted(["Elegoo", "Polymaker", "Bambu", "Hatchbox", "eSUN", "MultiLaser",
                "Creality", "Volt3D", "F3D", "GTMAX3D", "Anycubic"]):
                self.filament_brand.addItem(f_brand)
        f_grid.addWidget(self.filament_brand, 1, 1)
        f_grid.addWidget(QLabel("Cor"), 2, 0)
        self.filament_color = QComboBox()
        for color in sorted(["Azul", "Vermelho", "Branco", "Preto", "Amarelo", "Verde"]):
            self.filament_color.addItem(color)
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


class Print3DManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Print3D Manager")
        self.resize(1100, 800)
        self.setStyleSheet(STYLE_SHEET)

        # Layout Principal (HBox: Sidebar + Main Content)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.setup_sidebar(main_layout)
        self.setup_main_content(main_layout)

    def setup_sidebar(self, layout):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        sidebar.setGraphicsEffect(shadow)

        # Header Sidebar
        title = QLabel("Print3D Manager")
        title.setObjectName("MenuTitle")
        subtitle = QLabel("Controle de produção")
        subtitle.setObjectName("MenuSubtitle")
        
        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(subtitle)

        # Menu Items
        labels = [
            ("PRINCIPAL", False, None),
            ("Dashboard", True,  "res/img/icons/dashboard.png"),
            ("Nova peça", False,  "res/img/icons/3dpiece.png"),
            ("Histórico", False, "res/img/icons/history.png"),
            ("ESTOQUE", False, None),
            ("Filamentos", False, "res/img/icons/filament.png"),
            ("Relatórios", False, "res/img/icons/report.png"),
            ("Divider", False, None),
            ("Configurações", False, "res/img/icons/settings.png")
        ]

        for text, is_active, icon_path in labels:
            if text in ["PRINCIPAL", "ESTOQUE"]:
                lbl = QLabel(text)
                lbl.setStyleSheet("color: #888780;; font-size: 10px; letter-spacing: 1px; font-weight: bold; margin-top: 2px;")
                sidebar_layout.addWidget(lbl)
            elif text == "Divider":
                sidebar_layout.addWidget(make_divider())
            else:
                btn = QPushButton(f"  {text}")
                btn.setObjectName("MenuButton")
                btn.setProperty("active", str(is_active).lower())
                icon = QIcon(icon_path)
                btn.setIcon(icon)
                btn.setIconSize(QSize(18, 18))
                btn.setCursor(Qt.PointingHandCursor)
                sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        layout.addWidget(sidebar)

    def setup_main_content(self, layout):
        content_wrapper = QWidget()
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(32, 16, 32, 16)

        # Header com Botões
        header_layout = QHBoxLayout()
        header_title = QLabel("Nova peça — precificação")
        header_title.setStyleSheet("font-size: 20px; font-weight: 500; color: #FCFCFA;")
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setObjectName("PrimaryButton")
        btn_cancel.setFixedHeight(30)
        btn_cancel.setStyleSheet("""QPushButton:hover { background: #F12F28; color: #FCFCFA;}""")
        btn_save = QPushButton("Salvar peça")
        btn_save.setObjectName("PrimaryButton")
        btn_save.setStyleSheet("""QPushButton:hover { background: #2FF128; color: #2C2C2A;}""")
        
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_cancel)
        header_layout.addWidget(btn_save)
        content_layout.addLayout(header_layout)

        # --- Grid de Resumo (Cards Superiores) ---
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(16)
        
        summary_data = [
            ("Custo de material", "R$ 4,32", "#2563EB"),
            ("Custo de energia", "R$ 1,17", "#92400E"),
            ("Custo total", "R$ 7,49", "#1F2937"),
            ("Preço sugerido", "R$ 18,72", "#166534")
        ]

        for label, value, color in summary_data:
            card = QFrame()
            card.setObjectName("SummaryCard")
            card.setStyleSheet(f"border-radius: 8px; background-color: #fcfcfc;")
            v_lay = QVBoxLayout(card)
            lbl_descript = QLabel(label)
            lbl_descript.setStyleSheet("color: #666; font-size: 12px;")
            lbl_value = QLabel(value)
            lbl_value.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
            v_lay.addWidget(lbl_descript)
            v_lay.addWidget(lbl_value)
            summary_layout.addWidget(card)
        
        content_layout.addLayout(summary_layout)

        # --- Área Inferior (Dois Lados) ---
        bottom_layout = QHBoxLayout()
        
        # Lado Esquerdo: Dados da Peça
        left_card = QFrame()
        left_card.setProperty("class", "Card")
        left_lay = QVBoxLayout(left_card)
        
        left_lay.addWidget(QLabel("Dados da peça", objectName="CardTitle"))
        
        left_lay.addWidget(QLabel("Nome da peça"))
        name_input = QLineEdit()
        name_input.setPlaceholderText("Suporte de parede articulado")
        left_lay.addWidget(name_input)

        row2 = QHBoxLayout()
        v1 = QVBoxLayout()
        v1.addWidget(QLabel("Peso impresso (g)"));
        weight_input = QLineEdit()
        weight_input.setPlaceholderText("48")
        v1.addWidget(weight_input)
        v2 = QVBoxLayout()
        v2.addWidget(QLabel("Tempo de impressão"))
        time_input = QLineEdit()
        time_input.setPlaceholderText("3h20min")
        v2.addWidget(time_input)
        row2.addLayout(v1)
        row2.addLayout(v2)
        left_lay.addLayout(row2)

        row3 = QHBoxLayout()
        v3 = QVBoxLayout()
        v3.addWidget(QLabel("Infill (%)"))
        infill_input = QLineEdit()
        infill_input.setPlaceholderText("20")
        v3.addWidget(infill_input)
        v4 = QVBoxLayout()
        v4.addWidget(QLabel("Qualidade (mm)"))
        quality_input = QComboBox()
        for entry in ["0.2 mm (normal)", "0.1 mm (fina)", "0.3 mm (rápida)"]:
            quality_input.addItem(entry)
        v4.addWidget(quality_input)
        row3.addLayout(v3)
        row3.addLayout(v4)
        left_lay.addLayout(row3)

        left_lay.addWidget(QLabel("Cores utilizadas"))
        color_lay = QHBoxLayout()
        for color in ["#2563EB", "#EF4444"]:
            c_btn = QPushButton()
            c_btn.setFixedSize(24, 24)
            c_btn.setStyleSheet(f"background-color: {color}; border-radius: 10px; border: 1px solid #ccc;")
            color_lay.addWidget(c_btn)
        add_btn = QPushButton('+')
        add_btn.setFixedSize(20, 20)
        add_btn.setStyleSheet(f"background-color: #fcfcfc; border-radius: 10px; border: 1px solid #ccc;")
        color_lay.addWidget(add_btn)
        color_lay.addStretch()
        left_lay.addLayout(color_lay)

        left_lay.addWidget(QLabel("Observações"))
        observ_input = QTextEdit()
        left_lay.addWidget(observ_input)
        left_lay.addStretch()
        bottom_layout.addWidget(left_card, 6)

        # Lado Direito: Filamento e Custos
        right_column = QVBoxLayout()

        # Cards
        fil_card = FilamentCard()
        cost_card = CostCard()

        right_column.addWidget(fil_card)
        right_column.addWidget(cost_card)
        bottom_layout.addLayout(right_column, 4)

        content_layout.addLayout(bottom_layout)
        layout.addWidget(content_wrapper)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Print3DManager()
    window.show()
    sys.exit(app.exec())