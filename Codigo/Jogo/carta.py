from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import ImageTk, Image
from abc import ABC, abstractmethod

from .enums import CartaTipo
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Jogador

class Carta(ABC):
    def __init__(self, imagem: Image, tipo: CartaTipo):
        self.__imagem: Image = imagem
        self.__tipo: CartaTipo = tipo
    
    @property
    def idx(self):
        return self.__idx
    
    @property
    def imagem(self):
        return self.__imagem
    
    @property
    def tipo(self):
        return self.__tipo
    
    @staticmethod
    def ratio():
        return 315/500

    @abstractmethod
    def ativar(self, jogador: Jogador) -> None:
        pass

class Perdido(Carta):
    def __init__(self):
        super().__init__(imagem, CartaTipo.PERDIDO)

    def ativar(self, jogador: Jogador) -> None:
        pass

class Comprar(Carta):
    def __init__(self):
        super().__init__(imagem, CartaTipo.COMPRAR)

    def ativar(self, jogador: Jogador) -> None:
        pass

class BoaMira(Carta):
    def __init__(self):
        super().__init__(imagem, CartaTipo.BOAMIRA)

    def ativar(self, jogador: Jogador) -> None:
        pass