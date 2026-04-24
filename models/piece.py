from dataclasses import dataclass, field
from typing import List

from .filament import FilamentData


@dataclass
class PieceData:
    nome: str = ""
    peso_g: float = 0.0
    purga_g: float = 0.0
    tempo_horas: float = 0.0
    infill_pct: int = 20
    qualidade_mm: float = 0.2
    filamentos: List[FilamentData] = field(default_factory=list)
    observacoes: str = ""
    embalagem: float = 1.0

    # Estes dados não pertencem a peça mas as configurações de ambiente
    mao_de_obra: float = 2.0
    kwh_preco: float = 1.18
    potencia_kw: float = 0.30
    margem_pct: float = 150.0

    def custo_material(self) -> float:
        return sum(f.custo for f in self.filamentos)

    def custo_energia(self) -> float:
        return self.tempo_horas * self.potencia_kw * self.kwh_preco

    def custo_total(self, preco_grama: float) -> float:
        return (self.custo_material()
                + self.custo_energia()
                + self.mao_de_obra)

    def preco_venda(self, preco_grama: float) -> float:
        return self.custo_total(preco_grama) * (1 + self.margem_pct / 100)
