from datetime import date

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QDateEdit, QDialog, QDialogButtonBox,
QDoubleSpinBox, QFormLayout, QFrame, QGridLayout, QHBoxLayout, QLabel,
QLineEdit, QComboBox, QSpinBox, QVBoxLayout, QWidget)

from models.machine import MachineData
from ui.stylehelper import make_divider, make_section_label, STYLE_SHEET
from ui.styledmessagebox import StyledMessageBox


class AddMachineDialog(QDialog):
    """Dialog modal para adicionar uma nova máquina."""
 
    # Sinal alternativo — útil se preferir não usar exec()
    machine_added = Signal(MachineData)
 
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Nova máquina")
        self.setMinimumWidth(520)
        self.setModal(True)
        self.setStyleSheet(STYLE_SHEET)
 
        self._build_ui()
        self._connect_signals()
 
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 16)
        root.setSpacing(8)
        grid = QGridLayout()
        grid.setSpacing(8)
 
        # Título interno
        title = QLabel("Nova máquina")
        title.setObjectName("MenuTitle")
        root.addWidget(title)
 
        sub = QLabel("Preencha os dados da impressora")
        sub.setObjectName("MenuSubtitle")
        root.addWidget(sub)
        root.addWidget(make_divider())
        root.addStretch()
 
        # ── Formulário ──────────────────────────────────────────────
        self.f_modelo = QLineEdit()
        self.f_modelo.setPlaceholderText("Ex: K1")
        grid.addWidget(QLabel("Modelo *"), 0, 0)
        grid.addWidget(self.f_modelo, 1, 0)

        self.f_marca = QLineEdit()
        self.f_marca.setPlaceholderText("Ex: Creality")
        grid.addWidget(QLabel("Marca *"), 0, 1)
        grid.addWidget(self.f_marca, 1, 1)

        self.f_tipo = QComboBox()
        self.f_tipo.addItems(["FDM", "SLA / MSLA", "SLS", "DLP"])
        grid.addWidget(QLabel("Tipo"), 0, 2)
        grid.addWidget(self.f_tipo, 1, 2)

        self.f_preco = _money_spin(max_val=200_000)
        grid.addWidget(QLabel("Preço de compra (R$) *"), 2, 0)
        grid.addWidget(self.f_preco, 3, 0)

        self.f_potencia = QSpinBox()
        self.f_potencia.setRange(0, 5_000)
        self.f_potencia.setSuffix(" W")
        self.f_potencia.setValue(250)
        grid.addWidget(QLabel("Potência nominal (W)"), 2, 1)
        grid.addWidget(self.f_potencia, 3, 1)

        self.f_data = QDateEdit()
        self.f_data.setCalendarPopup(True)
        self.f_data.setDate(date.today())   # type: ignore[arg-type]
        self.f_data.setDisplayFormat("dd/MM/yyyy")
        grid.addWidget(QLabel("Data de compra"), 2, 2)
        grid.addWidget(self.f_data, 3, 2)

        self.f_amort = QSpinBox()
        self.f_amort.setRange(1, 240)
        self.f_amort.setSuffix(" meses")
        self.f_amort.setValue(24)
        grid.addWidget(QLabel("Amortização *"), 4, 0)
        grid.addWidget(self.f_amort, 5, 0)
 
        self.f_resid = _money_spin(max_val=200_000)
        grid.addWidget(QLabel("Valor residual (R$)"), 4, 1)
        grid.addWidget(self.f_resid, 5, 1)
 
        self.f_horas = QSpinBox()
        self.f_horas.setRange(1, 744)
        self.f_horas.setSuffix(" h/mês")
        self.f_horas.setValue(160)
        grid.addWidget(QLabel("Horas de uso / mês"), 4, 2)
        grid.addWidget(self.f_horas, 5, 2)
        root.addLayout(grid)

        # ── Banner custo/hora ────────────────────────────────────────
        self.cost_banner = make_section_label(
            "Custo/hora estimado: — aguardando dados"
            )
        root.addWidget(self.cost_banner)
 
        # ── Botões OK / Cancelar ─────────────────────────────────────
        root.addWidget(make_divider())
 
        btn_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        btn_box.button(QDialogButtonBox.Save).setText("Salvar máquina")
        btn_box.button(QDialogButtonBox.Save).setObjectName("PrimaryButton")
        btn_box.button(QDialogButtonBox.Cancel).setObjectName("GhostButton")
        btn_box.accepted.connect(self._on_accept)
        btn_box.rejected.connect(self.reject)
        root.addWidget(btn_box)
        root.addStretch()

    def _connect_signals(self):
        """Recalcula custo/hora sempre que qualquer campo numérico muda."""
        for widget in (self.f_preco, self.f_resid):
            widget.valueChanged.connect(self._update_cost)
        for widget in (self.f_potencia, self.f_amort, self.f_horas):
            widget.valueChanged.connect(self._update_cost)
 
    def _update_cost(self):
        data = self._read_form()
        custo = data.custo_hora
        if custo > 0:
            self.cost_banner.setText(
                f"⚡ Custo/hora estimado:  R$ {custo:.2f}"
            )
        else:
            self.cost_banner.setText("Custo/hora estimado: — aguardando dados")
 
    def _on_accept(self):
        errors = []
        if not self.f_modelo.text().strip():
            errors.append("• Modelo é obrigatório.")
        if not self.f_marca.text().strip():
            errors.append("• Marca é obrigatória.")
        if self.f_preco.value() <= 0:
            errors.append("• Preço de compra deve ser maior que zero.")
 
        if errors:
            StyledMessageBox.warning(self, "Campos obrigatórios", "\n".join(errors))
            return
 
        data = self._read_form()
        self.machine_added.emit(data)
        self.accept()
  
    def _read_form(self) -> MachineData:
        qdate = self.f_data.date()
        return MachineData(
            model = self.f_modelo.text().strip(),
            brand = self.f_marca.text().strip(),
            type = self.f_tipo.currentText(),
            preco = self.f_preco.value(),
            potencia_w = self.f_potencia.value(),
            data_compra = date(qdate.year(), qdate.month(), qdate.day()),
            amort_meses = self.f_amort.value(),
            valor_resid = self.f_resid.value(),
            horas_mes = self.f_horas.value(),
        )
 
    def get_data(self) -> MachineData:
        """Retorna os dados preenchidos. Chamar após exec() == Accepted."""
        return self._read_form()
 
# ─── Helpers privados ────────────────────────────────────────────────────────
 
def _money_spin(max_val: float = 99_999) -> QDoubleSpinBox:
    sp = QDoubleSpinBox()
    sp.setRange(0, max_val)
    sp.setDecimals(2)
    sp.setPrefix("R$ ")
    sp.setSingleStep(10)
    return sp
 
 
def _spacer() -> QFrame:
    """Linha vazia para separar grupos no QFormLayout."""
    f = QFrame()
    f.setFixedHeight(4)
    f.setFrameShape(QFrame.NoFrame)
    return f
 