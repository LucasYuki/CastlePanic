from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import ImageTk, Image
from abc import ABC, abstractmethod

if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Jogador

class Carta(ABC):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        self.__idx: str = idx
        self.__imagem: Image = imagem
        self.__tipo: str = tipo
    
    @property
    def idx(self):
        return self.__idx
    
    @property
    def imagem(self):
        return self.__imagem
    
    @property
    def tipo(self):
        return self.__tipo
    
    @property
    def ratio(self):
        return 315/500

    @abstractmethod
    def ativar(self, jogador: Jogador) -> None:
        pass

class Perdido(Carta):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)

    def ativar(self, jogador: Jogador) -> None:
        pass

class Comprar(Carta):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)

    def ativar(self, jogador: Jogador) -> None:
        pass

class BoaMira(Carta):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)

    def ativar(self, jogador: Jogador) -> None:
        pass