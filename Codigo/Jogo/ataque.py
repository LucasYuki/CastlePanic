from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import ImageTk, Image
from abc import ABC, abstractmethod

from Jogo.carta import BoaMira

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
        efeitos_pendentes: set = jogador.get_cartas_efeitos_pendentes()
        boa_mira = list(filter(type(BoaMira), efeitos_pendentes))
        if boa_mira != []:
            boa_mira = boa_mira[0] #Nao tenho certeza se da pra ter duas boas miras, se so da 1 fica mais facil
            jogador.remove_efeito_pendente(boa_mira)
        else:
            morto = monstro.danificar()
            if morto:
                pos.remover_monstro(monstro)
        jogador.remove_acao_pendente()

class Empurrao(Ataque):
    def __init__(self, tipo: CartaTipo):
        imagem = None # Colocar imagem de cada tipo de carta
        super().__init__(imagem, CartaTipo.EMPURRAO)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        pos.remover_monstro(monstro)
        jogador.mesa.colocar_peca(monstro, AnelTipo.FLORESTA , pos.fatia)
        jogador.remove_acao_pendente()

class Pixe(Ataque):
    def __init__(self, idx: str, imagem: Image, tipo: CartaTipo):
        imagem = None # Colocar imagem de cada tipo de carta
        super().__init__(imagem, CartaTipo.PIXE)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        monstro.imobilizar(jogador.mesa.get_turn())
        jogador.remove_acao_pendente()

class Barbaro(Ataque):
    def __init__(self, idx: str, imagem: Image, tipo: CartaTipo):
        imagem = None # Colocar imagem de cada tipo de carta
        super().__init__(imagem, CartaTipo.BARBARO)
    
    def agir(carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        pos.remover_monstro(monstro)
        jogador.remove_acao_pendente()