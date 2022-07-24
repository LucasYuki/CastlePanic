from __future__ import annotations
from typing import TYPE_CHECKING

from random import randrange
from abc import ABC, abstractmethod

from .enums import TokenTipo
from .token import Token
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Mesa

class Monstro(Token):
    def __init__(self, tipo: TokenTipo) -> None:
        if tipo == TokenTipo.GOBLIN:
            self._vida_max: int = 1
        elif tipo == TokenTipo.ORC:
            self._vida_max: int = 2
        elif tipo == TokenTipo.TROLL:
            self._vida_max: int = 3
        elif not TokenTipo.is_monstro_especial(tipo):
            raise ValueError("Tipo da monstro basico deve ser goblin, orc ou troll. Tipo recebido é %s" %str(carta_tipo))

        super().__init__(tipo)
        self.__vida: int = self._vida_max
        self.__ultimo_turno_imovel: int = -1

    def invocar(self, mesa: Mesa) -> None:
        mesa.get_tabuleiro().colocar_peca(self, 0, randrange(0,6))

    def danificar(self) -> bool:
        self.__vida -= 1
        return self.__vida <= 0

    def imovel(self, turno_atual: int) -> bool:
        return self.__ultimo_turno_imovel == turno_atual

    def imobilizar(self, turno_atual: int) -> None:
        self.__ultimo_turno_imovel = turno_atual

    def curar(self) -> None:
        if self.__vida < self._vida_max:
            self.__vida += 1

class Especial(Monstro, ABC):
    def __init__(self, vida_max: int, tipo: TokenTipo) -> None:
        self._vida_max = vida_max
        super().__init__(tipo)

    def invocar(self, mesa: Mesa) -> None:
        super().invocar(mesa)
        self.efeito(mesa)

    @abstractmethod
    def efeito(self, mesa: Mesa) -> None:
        pass

class Rei(Especial):
    def __init__(self) -> None:
        super().__init__(vida_max=3, tipo=TokenTipo.REI)

    def efeito(self, mesa: Mesa) -> None:
        tabuleiro = mesa.get_tabuleiro()
        for _ in range(3):
            tabuleiro.novo_token()

class Mago(Especial):
    def __init__(self) -> None:
        super().__init__(vida_max=2, tipo=TokenTipo.MAGO)

    def efeito(self, mesa: Mesa) -> None:
        mesa.get_tabuleiro().mover_montros()

class Medico(Especial):
    def __init__(self) -> None:
        super().__init__(vida_max=3, tipo=TokenTipo.MEDICO)

    def efeito(self, mesa: Mesa) -> None:
        mesa.get_tabuleiro().curar_todos()
