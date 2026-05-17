from dataclasses import dataclass, field
from datetime import date


@dataclass
class MachineData:
    brand: str = ""
    model: str = ""
    version: str = ""
    type: str = "FDM"
    colors: int = 1
    preco: float = 0.0
    potencia_w: int = 0
    data_compra: date = field(default_factory=date.today)
    amort_meses: int = 24
    valor_resid: float = 0.0
    horas_mes: int = 160

    @property
    def custo_hora(self) -> float:
        """Amortização linear simples + energia estimada."""
        if self.amort_meses <= 0 or self.horas_mes <= 0:
            return 0.0
        amort_total   = self.preco - self.valor_resid
        horas_total   = self.amort_meses * self.horas_mes   # horas de vida útil
        custo_amort   = amort_total / horas_total if horas_total else 0
        # energia: potência × tarifa média (R$1,07/kWh) — simplificado
        custo_energia = (self.potencia_w / 1000) * 1.07
        return round(custo_amort + custo_energia, 2)