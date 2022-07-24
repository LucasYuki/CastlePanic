from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import ImageTk, Image
from abc import ABC, abstractmethod

from .enums import CartaTipo
from Jogo import Carta
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Jogador
    from Jogo import Posicao
    from Jogo import Monstro

class Acao(Carta, ABC):
    def __init__(self, imagem: Image, tipo: CartaTipo):
        super().__init__(imagem, tipo)

    def ativar(self, jogador: Jogador) -> None:
        jogador.set_acao_pendente(self)

    @abstractmethod
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, 
            monstro: Monstro.Monstro = None) -> None:
        pass

class Reciclar(Acao):
    def __init__(self):
        imagem = Image.open("Images/base/C_scavenge.png")
        super().__init__(imagem, CartaTipo.RECICLAR)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        pass
        return super().agir(jogador, pos, monstro)

class Fortificar(Acao):
    def __init__(self):
        imagem = Image.open("Images/base/C_fortify.png")
        super().__init__(imagem, CartaTipo.FORTIFICAR)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        pass
        return super().agir(jogador, pos, monstro)

class ReparoMuro(Acao):
    def __init__(self, tipo: CartaTipo):
        if tipo == CartaTipo.MORTAR:
            imagem = Image.open("Images/base/C_mortar.png")
            super().__init__(imagem, tipo)
        if tipo == CartaTipo.TIJOLO:
            imagem = Image.open("Images/base/C_brick.png")
            super().__init__(imagem, tipo)

    def ativar(self, jogador: Jogador.Jogador) -> None:
        jogador.set_acao_pendente(self)
        return super().ativar(jogador)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        pass
        return super().agir(jogador, pos, monstro)