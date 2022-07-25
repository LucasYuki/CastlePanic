from __future__ import annotations
from typing import TYPE_CHECKING

from .peca import Fortificacao, Torre, Muro, Construcao
from .monstro import Monstro
from .enums import ContrucaoTipo

if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Peca
    from Jogo import Monstro
    from Jogo import AnelTipo
    from Jogo import Construcao

class Posicao:
    def __init__(self, fatia : int, anel : AnelTipo) -> None:
        self.__pecas: list[Peca] = []
        self.__fatia: int = fatia
        self.__anel: AnelTipo = anel

    @property
    def fatia(self):
        return self.__fatia

    @property
    def anel(self):
        return self.__anel

    @property
    def pecas(self):
        return self.__pecas

    def ha_torre(self) -> bool:
        return list(filter(lambda p: isinstance(p, Torre), self.__pecas)) != []

    def ha_construcao(self) -> bool:
        return list(filter(lambda p: isinstance(p, Construcao), self.__pecas)) != []

    def ha_muro(self) -> bool:
        return list(filter(lambda p: isinstance(p, Muro), self.__pecas)) != []
    
    def ha_fortificacao(self) -> bool:
        return list(filter(lambda p: isinstance(p, Fortificacao), self.__pecas)) != []

    def haMonstros(self) -> bool:
        monstros = list(filter(lambda p: isinstance(p, Monstro), self.__pecas))
        if monstros == []:
            return False
        return True

    def remover_monstro(self, monstro: Monstro) -> None:
        self.__pecas.remove(monstro)

    def destruir_construcao(self) -> None:
        construcoes = list(filter(lambda p: isinstance(p, Construcao), self.__pecas))
        tipos = list(map(lambda x: x.tipo, construcoes))
        for tipo in [ContrucaoTipo.FORTIFICACAO, ContrucaoTipo.MURO, ContrucaoTipo.TORRE]:
            if tipo in tipos:
                self.__pecas.remove(construcoes[tipos.index(tipo)])
                return

    def get_anel_fatia(self) -> tuple:
        return (self.__anel, self.__fatia)

    def remover_todos_monstros(self) -> None:
        for peca in self.__pecas:
            if isinstance(peca, Monstro):
                self.remover_monstro(peca)

    def curar_todos(self) -> None:
        monstros = filter(lambda p: isinstance(p, Monstro), self.__pecas)
        for monstro in monstros:
            monstro.curar()

    def colocar_peca(self, peca: Peca) -> None:
        self.__pecas.append(peca)

    def get_peca_id(self, monstro: Monstro):
        return self.__pecas.index(monstro)
        
    def get_peca_from_id(self, idx: int):
        return self.__pecas[idx]
    
    def get_info_dict(self):
        return {"anel": self.__anel, "fatia": self.__fatia}
    