from dataclasses import dataclass


@dataclass
class Citta:
    nome: str
    giorniTot: int
    giorniCons: int
    listaSituazioni: list


