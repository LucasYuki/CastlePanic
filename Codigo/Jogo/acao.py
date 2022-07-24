from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import ImageTk, Image
from abc import ABC, abstractmethod

from Jogo import Carta
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Jogador
    from Jogo import Posicao
    from Jogo import Monstro

class Acao(Carta, ABC):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)

    def ativar(self, jogador: Jogador.Jogador) -> None:
        pass

    @abstractmethod
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, 
            monstro: Monstro.Monstro = None) -> None:
        pass

class Reciclar(Acao):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)

    def ativar(self, jogador: Jogador.Jogador) -> None:
        pass
        return super().ativar(jogador)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, monstro: Monstro.Monstro = None) -> None:
        pass
        return super().agir(jogador, pos, monstro)

class Fortificar(Acao):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)

    def ativar(self, jogador: Jogador.Jogador) -> None:
        pass
        return super().ativar(jogador)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, monstro: Monstro.Monstro = None) -> None:
        pass
        return super().agir(jogador, pos, monstro)

class ReparoMuro(Acao):
    def __init__(self, idx: str, imagem: Image, tipo: str):
        super().__init__(idx, imagem, tipo)

    def ativar(self, jogador: Jogador.Jogador) -> None:
        pass
        return super().ativar(jogador)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, monstro: Monstro.Monstro = None) -> None:
        pass
        return super().agir(jogador, pos, monstro)