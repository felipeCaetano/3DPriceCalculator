from dataclasses import dataclass, field
from typing import List


@dataclass
class PieceData:
    nome: str = ""
    peso_g: float = 0.0
    tempo_horas: float = 0.0
    infill_pct: int = 20
    qualidade_mm: float = 0.2
    cores: List[str] = field(default_factory=list)
    observacoes: str = ""
    mao_de_obra: float = 2.0
    kwh_preco: float = 1.18
    potencia_kw: float = 0.30
    margem_pct: float = 150.0

    def custo_material(self, preco_grama: float) -> float:
        return self.peso_g * preco_grama

    def custo_energia(self) -> float:
        return self.tempo_horas * self.potencia_kw * self.kwh_preco

    def custo_total(self, preco_grama: float) -> float:
        return (self.custo_material(preco_grama)
                + self.custo_energia()
                + self.mao_de_obra)

    def preco_venda(self, preco_grama: float) -> float:
        return self.custo_total(preco_grama) * (1 + self.margem_pct / 100)
