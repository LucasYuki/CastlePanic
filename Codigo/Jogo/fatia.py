from __future__ import annotations
from typing import TYPE_CHECKING

from .enums import AnelTipo, FatiaCor
from .posicao import Posicao
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Peca
    from Jogo import Monstro

class Fatia:
    def __init__(self, num: int) -> None:
        self.__aneis: dict[Posicao] = {anel: Posicao(fatia=num, anel=anel) for anel in AnelTipo.list()}
        self.__cor: int = FatiaCor.num2cor(num)
        self.__num: int = num

    @property
    def num(self):
        return self.__num

    @property
    def aneis(self):
        return self.__aneis

    def verificar_torres_destruidas(self) -> bool:
        for posicao in self.__aneis.values():
            if posicao.ha_torre():
               return False 
        return True

    def haMonstros(self) -> bool:
        for posicao in self.__aneis.values():
            if posicao.haMonstros():
                return True
        return False

    # ACHO QUE EH ISSO
    def ha_construcoes(self, destino: Posicao) -> bool:
        return destino.ha_construcao()

    def get_posicao(self, anel: AnelTipo) -> Posicao:
        return self.__aneis[anel]

    def pedra_entrando(self) -> bool:
        for anel, posicao in self.__aneis.items():
            if anel != AnelTipo.CASTELO: # A posicao nao eh a do castelo
                posicao.remover_todos_monstros()
                continue
            
            atravessou: bool = not posicao.ha_construcao()
            if atravessou:
                posicao.remover_todos_monstros()
            else:
                posicao.destruir_construcao()
            return atravessou

    def pedra_saindo(self) -> None:
        # Tira todos os monstros de dentro do castelo
        castelo = self.__aneis[AnelTipo.CASTELO]
        castelo.remover_todos_monstros()
        atravessou_tudo: bool = not castelo.ha_construcao()
        # Destroi uma construcao no castelo
        if not atravessou_tudo:
            castelo.destruir_construcao()
            return
        
        # Se nao tinha
        for posicao in self.__aneis.values():
            posicao.remover_todos_monstros()

    def curar_todos(self) -> None:
        for posicao in self.__aneis.values():
            posicao.curar_todos()

    def colocar_peca(self, peca: Peca, anel: AnelTipo) -> None:
        self.__aneis[anel].colocar_peca(peca)