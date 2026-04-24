from dataclasses import dataclass


@dataclass
class Machine:
    nome: str = ""
    model: str = ""
    version: str = ""
    potencia_kw: float = .3
    colors: int = 1