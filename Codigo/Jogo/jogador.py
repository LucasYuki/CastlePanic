from __future__ import annotations
from typing import TYPE_CHECKING

from random import randrange

from urllib.parse import ParseResultBytes

from Jogo.enums import CartaTipo
from Jogo.token import Descarta

if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Carta
    from Jogo import Mesa
    from Jogo import Acao

class Jogador():
    def __init__(self, nome: str, idx: str, ordem: str, mesa: Mesa):
        self.__mao: list[Carta] = []
        
        # Nao ta no diagrama de classes
        self.idx = idx
        self.nome = nome
        self.ordem = ordem
        # Fim

        self.__pontos: int  = None
        self.__mesa: Mesa = mesa
        self.__acao_pendente: Acao = None #Mudar Carta para Acao
        self.__carta_efeito_pendente: set[Carta] = set()
        
    @property
    def mesa(self):
        return self.__mesa
    
    # NAO MEXI NISSO
    def colocar_na_mao(self, carta: Carta):
        self.__mao.append(carta)

    def comprar_carta(self) -> None:
        carta = self.__mesa.get_carta_compra()
        if carta:
            self.colocar_na_mao(carta)

    def comprar_mao(self) -> None:
        n_cards: int = Mesa.mesa.get_num_cartas()
        while len(self.__mao) < n_cards:
            self.comprar_carta()

    def tirar_da_mao(self, carta: Carta) -> Carta:
        self.__mao.remove(carta)

    def possui_carta(self, carta: Carta) -> bool:
        return carta in self.__mao

    def propor_troca(self) -> None:
        pass

    def descartar(self, carta: Carta) -> bool:
        if not carta in self.__mao:
            return False
        self.__mao.remove(carta)
        self.__mesa.put_descarte(carta)
        return True

    # Acho que ta certo
    def descartar_aleatoria(self) -> None:
        if self.__mao == []:
            return
        self.__mao.pop(randrange(0, len(self.__mao)))
        

    def descartar_todas(self, carta_tipo: CartaTipo) -> None:
        self.__mao = list(filter(lambda x: x.tipo != carta_tipo, self.__mao))

    def set_acao_pendente(self, carta: Carta) -> None:
        self.__acao_pendente = carta

    def remove_acao_pendente(self) -> None:
        self.descartar(self.__acao_pendente)
        self.__acao_pendente = None

    def get_acao_pendente(self) -> Carta:
        return self.__acao_pendente

    def add_carta_efeito_pendente(self, carta: Carta) -> None:
        self.__carta_efeito_pendente.add(carta)

    def remove_efeito_pendente(self, carta: Carta) -> None:
        self.__carta_efeito_pendente.remove(carta)
        self.descartar(carta)

    def get_cartas_efeitos_pendentes(self) -> set:
        return self.__carta_efeito_pendente

    def encerra_turno(self) -> None:
        self.__acao_pendente = None
        self.__carta_efeito_pendente.clear()

    def get_mao(self) -> None: #Mudar o returno aqui?
        return self.__mao
