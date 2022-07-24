from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import ImageTk, Image
from abc import ABC, abstractmethod

from Jogo import Acao
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Carta
    from Jogo import Jogador
    from Jogo import Monstro
    from Jogo import Posicao

class Ataque(Acao, ABC):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)
        self.__anel: set[int] = set()
        self.__cor: set[int] = set()

    def ativar(self, jogador: Jogador.Jogador) -> None:
        return super().ativar(jogador)
        pass

    @abstractmethod
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, monstro: Monstro.Monstro = None) -> None:
        pass

    def aplicar_ataque(monstro: Monstro.Monstro) -> None:
        pass

    def verificar_alcance(self, pos: Posicao.Posicao) -> bool:
        pass

class Dano(Ataque):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)
        self.__dano: int = None
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, monstro: Monstro.Monstro = None) -> None:
        return super().agir(jogador, pos, monstro)

class Empurrao(Ataque):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, monstro: Monstro.Monstro = None) -> None:
        return super().agir(jogador, pos, monstro)

class Pixe(Ataque):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, monstro: Monstro.Monstro = None) -> None:
        return super().agir(jogador, pos, monstro)

class Barbaro(Ataque):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, monstro: Monstro.Monstro = None) -> None:
        return super().agir(jogador, pos, monstro)