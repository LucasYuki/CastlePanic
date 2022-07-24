from __future__ import annotations
from typing import TYPE_CHECKING

from urllib.parse import ParseResultBytes

if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Carta
    from Jogo import Mesa

class Jogador():
    def __init__(self, nome: str, idx: str, ordem: str):
        self.__mao: list[Carta] = []
        
        # Nao ta no diagrama de classes
        self.idx = idx
        self.nome = nome
        self.ordem = ordem
        # Fim

        self.__pontos: int  = None
        self.__mesa: Mesa = None
        self.__acao_pendente: Carta = None #Mudar Carta para Acao
        self.__carta_efeito_pendente: set[Carta] = set()
        
    @property
    def mesa(self):
        return self.__mesa
    
    # NAO MEXI NISSO
    def colocar_na_mao(self, carta: Carta):
        self.__mao.append(carta)

    def comprar_carta(self) -> None:
        carta = Mesa.mesa.get_carta_compra()
        if carta:
            self.colocar_na_mao(carta)

    def comprar_mao(self) -> None:
        n_cards: int = Mesa.mesa.get_num_cartas()
        while len(self.__mao) < n_cards:
            self.comprar_carta()

    def tirar_da_mao(self, carta: Carta) -> Carta:
        pass

    def possui_carta(self, carta: Carta) -> bool:
        return carta in self.__mao

    def propor_troca(self) -> None:
        pass

    def descartar(self, carta: Carta) -> bool:
        self.__mao.remove(carta)

    def descartar_escolhida(self, carta_nome: str) -> None:
        pass

    def descartar_todas(self, carta_nome: str) -> None:
        # Entradas possiveis: arqueiro, espadachin, cavaleiro
        pass

    def set_acao_pendente(self, carta: Carta) -> None:
        pass

    def remove_acao_pendente(self) -> None:
        self.descartar(self.__acao_pendente)
        self.__acao_pendente = None

    def get_acao_pendente(self) -> Carta:
        pass

    def add_carta_efeito_pendente(self, carta: Carta) -> None:
        pass

    def remove_efeito_pendente(self, carta: Carta) -> None:
        self.__carta_efeito_pendente.remove(carta)
        self.descartar(carta)

    def get_cartas_efeitos_pendentes(self) -> None:
        return self.__carta_efeito_pendente

    def encerra_turno(self) -> None:
        pass # kkkkk

    def get_mao(self) -> None: #Mudar o returno aqui?
        return self.__mao
