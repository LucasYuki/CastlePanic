from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import Image
from abc import ABC, abstractmethod

from .enums import ContrucaoTipo
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    # from Jogo import Jogador
    pass
    
class Peca(ABC):
    __imagem : Image

    def __init__(self):
        super().__init__()
        self.__imagem = self.load_image() 
        if not self.__imagem:
            raise ValueError("Imagem não carregada.")

    def get_image(self):# -> Image
        return self.__imagem

    @abstractmethod
    def load_image(self):# -> Image
        pass

class Construcao(Peca):
    _prioridade: int
    _tipo: ContrucaoTipo
    
    def __init__(self):
        super().__init__()
        self.__prioridade: int = None

    @property
    def prioridade(self) -> int:
        return self._prioridade
    
    @property
    def tipo(self) -> ContrucaoTipo:
        return self._tipo

class Torre(Construcao):
    def __init__(self) -> None:
        super().__init__()
        self._prioridade: int = 1
        self._tipo = ContrucaoTipo.TORRE
        
    def load_image(self):
        return Image.open("Images/base/Torre2.png")

class Muro(Construcao):
    def __init__(self) -> None:
        super().__init__()
        self._prioridade: int = 2
        self._tipo = ContrucaoTipo.MURO
    
    def load_image(self):
        return Image.open("Images/base/Muro2.png")

class Fortificacao(Construcao):
    def __init__(self) -> None:
        super().__init__()
        self._prioridade: int = 3
        self._tipo = ContrucaoTipo.FORTIFICACAO
    
    def load_image(self):
        return Image.open("Images/base/Fortificacao.png")
