from __future__ import annotations
from typing import TYPE_CHECKING

from random import randrange
from abc import ABC, abstractmethod

from .enums import TokenTipo, CartaTipo
from .peca import Peca
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Carta
    from Jogo import Mesa

class Token(Peca):
    def __init__(self, tipo: TokenTipo) -> None:
        self.__tipo = tipo
        super().__init__()
        
    def load_image(self): # -> Image
        pass

    @abstractmethod
    def invocar(self, mesa: Mesa):
        pass

class ComprarTokens(Token):
    def __init__(self, n_tokens: int) -> None:
        if n_tokens == 3:
            super().__init__(TokenTipo.COMPRAR_TOKEN_3)
        elif n_tokens == 4:
            super().__init__(TokenTipo.COMPRAR_TOKEN_4)
        else:
            raise ValueError("Número de tokens deve ser 3 ou 4. Valor recebido %s" %str(n_tokens))
        self.__n_tokens: int = n_tokens

    def invocar(self, mesa: Mesa.Mesa):
        tabuleiro = mesa.get_tabuleiro()
        for _ in range(self.__n_tokens):
            tabuleiro.novo_token()
    
    def load_image(self): # -> Image
        pass

class Descarta(Token):
    def __init__(self) -> None:
        super().__init__(TokenTipo.DESCARTA)

    def invocar(self, mesa: Mesa.Mesa):
        pass

class Pedra(Token):
    def __init__(self) -> None:
        super().__init__(TokenTipo.PEDRA)

    def invocar(self, mesa: Mesa.Mesa):
        fatia: int = randrange(0,6)
        mesa.get_tabuleiro().pedra(fatia)

class Praga(Token):
    def __init__(self, carta_tipo: CartaTipo) -> None:
        if carta_tipo == CartaTipo.ARQUEIRO: 
            super().__init__(TokenTipo.PRAGA_ARQUEIROS)
        elif carta_tipo == CartaTipo.CAVALEIRO:
            super().__init__(TokenTipo.PRAGA_CAVALEIRO)
        elif carta_tipo == CartaTipo.ESPADACHIM:
            super().__init__(TokenTipo.PRAGA_ESPADACHIM)
        else:
            raise ValueError("Tipo da carta deve ser arqueito, cavaleiro ou espadachim. Tipo recebido é %s" %str(carta_tipo))
        self.__carta_tipo: CartaTipo = carta_tipo

    def invocar(self, mesa: Mesa.Mesa):
        mesa.descartar_todas(self.__carta_tipo)