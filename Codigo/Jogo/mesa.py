from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import ImageTk, Image, ImageDraw
import numpy as np

from .enums import TokenTipo, CartaTipo, AnelTipo
from .tabuleiro import Tabuleiro
from .jogador import Jogador
from .carta import Comprar
from .monstro import Monstro, Rei, Mago, Medico
from .token import ComprarTokens, Descarta, Pedra, Praga
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Token
    from Jogo import Monstro
    from Jogo import Posicao
    from Jogo import Peca

class Mesa():
    def __init__(self, jogadores, seed: int):    
        self.__turno: int = 0
        self.__fase: str = None
        self.__jogador_no_controle: str = None
        self.__tokens_bloqueados: bool = False
        self.__subestado: str = False
        
        self.__tabuleiro = Tabuleiro()
        self.__descarte_tokens: list[Token.Token] = []
        self.__pilha_cartas: list[Carta.Carta] = []
        self.__pilha_descarte: list[Carta.Carta] = []
        self.__saco_tokens: list[Token] = []
        
        # Inicializa Tokens
        monstros_iniciais: list[Monstro] = []
        
        # 6 Goblins
        monstros_iniciais += [Monstro(TokenTipo.GOBLIN) for i in range(3)]
        self.__saco_tokens += [Monstro(TokenTipo.GOBLIN) for i in range(3)]
        # 11 Orcs
        monstros_iniciais += [Monstro(TokenTipo.ORC) for i in range(2)]
        self.__saco_tokens += [Monstro(TokenTipo.ORC) for i in range(9)]
        # 10 Trolls
        monstros_iniciais.append(Monstro(TokenTipo.TROLL))
        self.__saco_tokens += [Monstro(TokenTipo.TROLL) for i in range(9)]
        # 1 Goblin King
        self.__saco_tokens.append(Rei())
        # 1 Troll Mage
        self.__saco_tokens.append(Mago())
        # 1 Healer
        self.__saco_tokens.append(Medico())
        # 1 Plague! Swordsmen
        self.__saco_tokens.append(Praga(CartaTipo.ESPADACHIM))
        # 1 Plague! Knights
        self.__saco_tokens.append(Praga(CartaTipo.CAVALEIRO))
        # 1 Plague! Archers
        self.__saco_tokens.append(Praga(CartaTipo.ARQUEIRO))
        # 1 All Players Discard 1 Card
        self.__saco_tokens.append(Descarta())
        # 4 Giant Boulder
        self.__saco_tokens += [Pedra() for i in range(4)]
        # 1 Draw 3 Monster Tokens
        self.__saco_tokens.append(ComprarTokens(3))
        # 1 Draw 4 Monster Tokens
        self.__saco_tokens.append(ComprarTokens(4))
        
        np.random.seed(seed)
        np.random.permutation(self.__saco_tokens)
        np.random.permutation(monstros_iniciais)
        for fatia, monstro_inicial in enumerate(monstros_iniciais):
            self.__tabuleiro.colocar_peca(monstro_inicial, AnelTipo.CASTELO, fatia)

        # Inicializa Jogadores
        self.__jogadores: dict[Jogador] = {info[1]: Jogador(*info) for info in jogadores}
        
        # Inicializa Cartas
        """
        # Inicialização das imagens das cartas
        orig_img = Image.open("Images/base/49Cartas.jpg")
        
        card_mask = Image.new("1", (315, 500), (0))
        tmp_draw = ImageDraw.Draw(card_mask)
        tmp_draw.rounded_rectangle((0, 0, 315, 500), fill=1, outline=1,
                                   width=0, radius=25)
        
        y = 0
        for idx in self.__jogadores:
            for x in range(6):
                carta_img = orig_img.crop((327*x+5, 510*y+5, 327*(x+1)-7, 510*(y+1)-5))
                carta_img.putalpha(card_mask) 
                self.__jogadores[idx].colocar_na_mao(Comprar())
            y += 1
        """
    
    @property
    def jogadores(self):
        return self.__jogadores

    @property
    def turno(self):
        return self.__turno

    def get_carta_compra(self) -> Carta.Carta:
        pass

    def put_descarte(self, carta: Carta.Carta) -> None:
        pass

    def get_num_cartas(self) -> int:
        pass

    def get_turn(self) -> int:
        pass

    def get_tabuleiro(self) -> Tabuleiro.Tabuleiro:
        return self.__tabuleiro

    def set_turno(self, jogador: Jogador) -> None:
        pass

    def passar_jogada(self, jogador_id: str) -> bool:
        pass

    def descartar_compra(self, carta: Carta, jogador_id: str) -> bool:
        pass

    def selecionar_carta_descarte(self, carta: Carta, jogador: Jogador) -> bool:
        pass

    def selecionar_monstro(self, monstro: Monstro.Monstro, pos: Posicao.Posicao, jogador: Jogador) -> bool:
        pass

    def selecionar_posicao(self, pos: Posicao.Posicao, jogador: Jogador) -> bool:
        pass

    def jogar_carta(self, carta: Carta.Carta, jogador: Jogador) -> bool:
        pass

    def troca(self, carta_atual: Carta.Carta, carta_troca: Carta.Carta, jogador_atual: Jogador, jogador_troca: Jogador) -> bool:
        pass

    def resposta_troca(self, jogador_troca: Jogador, resposta: bool) -> bool:
        pass

    def declarar_vitoria(self) -> None:
        pass

    def declarar_derrota(self) -> None:
        pass

    def proximo_jogador(self) -> None:
        pass

    def descartar_todas(self, carta_tipo: str) -> None:
        # Entradas possiveis: arqueiro, espadachin, cavaleiro
        for jogador in self.__jogadores:
            jogador.descartar_todas(carta_tipo)
        pass

    def todos_descartam_um(self) -> None:
        pass

    def bloquear_tokens(self) -> None:
        pass

    def colocar_peca(self, peca: Peca.Peca, anel: int, fatia: int) -> None:
        pass

    def get_token(self) -> Token:
        if self.__tokens_bloqueados or not len(self.__saco_tokens):
            return None
        return self.__saco_tokens.pop()
