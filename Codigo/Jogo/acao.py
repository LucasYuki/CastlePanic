from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import ImageTk, Image
from abc import ABC, abstractmethod

from .peca import Fortificacao, Muro

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
    def agir(self, carta: Carta = None, jogador: Jogador = None, pos: Posicao.Posicao = None, 
            monstro: Monstro.Monstro = None) -> None:
        pass #ABC

class Reciclar(Acao):
    def __init__(self):
        imagem = Image.open("Images/base/C_scavenge.png")
        super().__init__(imagem, CartaTipo.RECICLAR)
    
    def agir(self, carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        jogador.colocar_na_mao(carta)
        jogador.remove_acao_pendente()

class Fortificar(Acao):
    def __init__(self):
        imagem = Image.open("Images/base/C_fortify.png")
        super().__init__(imagem, CartaTipo.FORTIFICAR)
    
    def agir(self, carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        fortificacao = Fortificacao()
        jogador.mesa.colocar_peca(fortificacao, pos.anel, pos.fatia)
        jogador.remove_acao_pendente()

class ReparoMuro(Acao):
    def __init__(self, tipo: CartaTipo):
        if tipo == CartaTipo.MORTAR:
            imagem = Image.open("Images/base/C_mortar.png")
            super().__init__(imagem, tipo)
        if tipo == CartaTipo.TIJOLO:
            imagem = Image.open("Images/base/C_brick.png")
            super().__init__(imagem, tipo)

    def ativar(self, jogador: Jogador) -> None:
        efeitos = map(lambda carta: carta.tipo ,jogador.get_cartas_efeitos_pendentes())
        if self.tipo == CartaTipo.MORTAR and CartaTipo.TIJOLO in efeitos:
            jogador.set_acao_pendente(self)
        elif self.tipo == CartaTipo.TIJOLO and CartaTipo.MORTAR in efeitos:
            jogador.set_acao_pendente(self)
        else:
            jogador.add_carta_efeito_pendente(self)
    
    def agir(self, carta: Carta = None, jogador: Jogador = None, pos: Posicao = None, monstro: Monstro = None) -> None:
        muro = Muro()
        jogador.mesa.colocar_peca(muro, pos.anel, pos.fatia)
        efeitos = jogador.get_cartas_efeitos_pendentes()
        tipo_oposto = CartaTipo.TIJOLO if self.tipo == CartaTipo.MORTAR else CartaTipo.MORTAR
        carta_oposta = list(filter(lambda x: x.tipo == tipo_oposto, efeitos))
        jogador.remove_efeito_pendente(carta_oposta[0])
        jogador.remove_acao_pendente()
