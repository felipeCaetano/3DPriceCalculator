from dataclasses import dataclass


@dataclass
class FilamentData:
    tipo: str = "PLA"
    marca: str = "Polymaker"
    cor: str = "Azul royal"
    preco_kg: float = 89.90
    peso_bobina_g: float = 1000.0
    peso_usado_g: float = 380.0

    @property
    def preco_grama(self) -> float:
        return self.preco_kg / 1000

    @property
    def bobina_restante_pct(self) -> int:
        restante = self.peso_bobina_g - self.peso_usado_g
        return int((restante / self.peso_bobina_g) * 100)
