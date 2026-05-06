from dataclasses import dataclass


@dataclass
class FilamentData:
    tipo: str = "PLA"
    acabamento: str = "Sólido"
    marca: str = "Polymaker"
    cor: str = "Azul royal"
    cor_str: str = ""
    preco_kg: float = 89.90
    peso_g: float = 0.0          # quanto desta cor foi usado na peça
    peso_bobina_g: float = 1000.0
    peso_usado_g: float = 380.0
    data_validade: str = ""
    data_abertura: str = ""
    quantidade: int = 0

    @property
    def preco_grama(self) -> float:
        return self.preco_kg / 1000
    
    @property
    def custo(self) -> float:
        return self.peso_g * self.preco_grama

    @property
    def bobina_restante_pct(self) -> int:
        if self.peso_bobina_g <= 0 and self.quantidade == 0:
            return 0
        restante = (self.peso_bobina_g  * self.quantidade) - self.peso_usado_g
        return max(0, int((restante / self.peso_bobina_g) * 100))
    
    def registrar_uso(self):
        self.peso_usado_g += self.peso_g
