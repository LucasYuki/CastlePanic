from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Peca
    from Jogo import Monstro
    from Jogo import AnelTipo

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
        pass

    def haMonstros(self) -> bool:
        monstros = filter(isinstance(Monstro), self.__pecas)
        if monstros == []:
            return False
        return True

    def ha_construcao(self) -> bool:
        pass

    def remover_monstro(self, monstro: Monstro) -> None:
        self.__pecas.remove(monstro)

    def destruir_construcao(self) -> None:
        pass

    def get_anel_fatia(self) -> tuple:
        return (self.__anel, self.__fatia)

    def novo_monstro(self, monstro: Monstro) -> None:
        pass

    def remover_todos_monstros(self) -> None:
        for peca in self.__pecas:
            if isinstance(peca, Monstro):
                self.remover_monstro(peca)

    def curar_todos(self) -> None:
        monstros = filter(isinstance(Monstro), self.__pecas)
        for monstro in monstros:
            monstro.curar()

    def colocar_peca(self, peca: Peca) -> None:
        self.__pecas.append(peca)
