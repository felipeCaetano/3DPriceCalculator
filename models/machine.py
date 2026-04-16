from dataclasses import dataclass, field
from typing import List


@dataclass
class Machine:
    nome: str = ""
    model: str = ""
    version: str = ""
    potencia_kw: float = .3
    colors: int = 1