from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import ImageTk, Image
from abc import ABC, abstractmethod

from .enums import CartaTipo, AnelTipo, FatiaCor
from Jogo import Acao
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Carta
    from Jogo import Jogador
    from Jogo import Monstro
    from Jogo import Posicao

class Ataque(Acao, ABC):
    def __init__(self, imagem: Image, tipo: CartaTipo, aneis: set, cores: FatiaCor):
        super().__init__(imagem, tipo)
        self.__anel: set[AnelTipo] = aneis
        self.__cor: FatiaCor = cores

    def ativar(self, jogador: Jogador) -> None:
        return super().ativar(jogador)
        pass

    @abstractmethod
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        pass

    def aplicar_ataque(monstro: Monstro) -> None:
        pass

    def verificar_alcance(self, pos: Posicao) -> bool:
        pass

class Dano(Ataque):
    def __init__(self, tipo: CartaTipo, cor: FatiaCor):
        imagem = None # Colocar imagem de cada tipo de carta
        if tipo == CartaTipo.ARQUEIRO:
            if cor == FatiaCor.VERMELHO:
                super().__init__(imagem, tipo, {AnelTipo.ARQUEIRO}, cor)
            elif cor == FatiaCor.VERDE:
                super().__init__(imagem, tipo, {AnelTipo.ARQUEIRO}, cor)
            elif cor == FatiaCor.AZUL:
                super().__init__(imagem, tipo, {AnelTipo.ARQUEIRO}, cor)
            elif cor == FatiaCor.TODAS:
                super().__init__(imagem, tipo, {AnelTipo.ARQUEIRO}, cor)
        elif tipo == CartaTipo.CAVALEIRO:
            if cor == FatiaCor.VERMELHO:
                super().__init__(imagem, tipo, {AnelTipo.CAVALEIRO}, cor)
            elif cor == FatiaCor.VERDE:
                super().__init__(imagem, tipo, {AnelTipo.CAVALEIRO}, cor)
            elif cor == FatiaCor.AZUL:
                super().__init__(imagem, tipo, {AnelTipo.CAVALEIRO}, cor)
            elif cor == FatiaCor.TODAS:
                super().__init__(imagem, tipo, {AnelTipo.CAVALEIRO}, cor)
        elif tipo == CartaTipo.ESPADACHIM:
            if cor == FatiaCor.VERMELHO:
                super().__init__(imagem, tipo, {AnelTipo.ESPADACHIM}, cor)
            elif cor == FatiaCor.VERDE:
                super().__init__(imagem, tipo, {AnelTipo.ESPADACHIM}, cor)
            elif cor == FatiaCor.AZUL:
                super().__init__(imagem, tipo, {AnelTipo.ESPADACHIM}, cor)
            elif cor == FatiaCor.TODAS:
                super().__init__(imagem, tipo, {AnelTipo.ESPADACHIM}, cor)
        elif tipo == CartaTipo.HEROI:
            aneis_heroi = {AnelTipo.ARQUEIRO, AnelTipo.CAVALEIRO, AnelTipo.ESPADACHIM}
            if cor == FatiaCor.VERMELHO:
                super().__init__(imagem, tipo, aneis_heroi, cor)
            elif cor == FatiaCor.VERDE:
                super().__init__(imagem, tipo, aneis_heroi, cor)
            elif cor == FatiaCor.AZUL:
                super().__init__(imagem, tipo, aneis_heroi, cor)
            else:
                raise ValueError("O heroí deve ser de uma das cores, não exite herói de todas as cores")
        else:
            raise ValueError("Tipo da carta dano deve ser arqueiro, cavaleiro, espadachim ou heroi. Tipo recebido é %s" %str(carta_tipo))
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        return super().agir(jogador, pos, monstro)

class Empurrao(Ataque):
    def __init__(self, tipo: CartaTipo):
        imagem = None # Colocar imagem de cada tipo de carta
        super().__init__(imagem, CartaTipo.EMPURRAO)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        return super().agir(jogador, pos, monstro)

class Pixe(Ataque):
    def __init__(self, idx: str, imagem: Image, tipo: CartaTipo):
        imagem = None # Colocar imagem de cada tipo de carta
        super().__init__(imagem, CartaTipo.PIXE)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        return super().agir(jogador, pos, monstro)

class Barbaro(Ataque):
    def __init__(self, idx: str, imagem: Image, tipo: CartaTipo):
        imagem = None # Colocar imagem de cada tipo de carta
        super().__init__(imagem, CartaTipo.BARBARO)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        return super().agir(jogador, pos, monstro)