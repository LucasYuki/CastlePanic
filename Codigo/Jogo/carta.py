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
        pass #ABC

class Perdido(Carta):
    def __init__(self):
        imagem = Image.open("Images/base/C_missing.png")
        super().__init__(imagem, CartaTipo.PERDIDO)

    def ativar(self, jogador: Jogador) -> None:
        jogador.mesa.bloquear_tokens()
        jogador.descartar(self)

class Comprar(Carta):
    def __init__(self):
        imagem = Image.open("Images/base/C_draw.png")
        super().__init__(imagem, CartaTipo.COMPRAR)

    def ativar(self, jogador: Jogador) -> None:
        for _ in range(2):
            jogador.comprar_carta()
        jogador.descartar(self)

class BoaMira(Carta):
    def __init__(self):
        imagem = Image.open("Images/base/C_nice_shot.png")
        super().__init__(imagem, CartaTipo.BOAMIRA)

    def ativar(self, jogador: Jogador) -> None:
        jogador.add_carta_efeito_pendente(self)