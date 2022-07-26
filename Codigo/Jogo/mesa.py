from __future__ import annotations
from doctest import FAIL_FAST
from typing import TYPE_CHECKING

from PIL import ImageTk, Image, ImageDraw
import numpy as np

from .enums import TokenTipo, CartaTipo, AnelTipo, FatiaCor, FaseTipo
from .tabuleiro import Tabuleiro
from .jogador import Jogador

# cartas 
from .ataque import Dano, Empurrao, Pixe, Barbaro, Ataque
from .carta import Perdido, Comprar, BoaMira
from .acao import Acao, Reciclar, Fortificar, ReparoMuro

# tokens
from .monstro import Monstro, Rei, Mago, Medico
from .token import ComprarTokens, Descarta, Pedra, Praga

if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Token
    from Jogo import Monstro
    from Jogo import Posicao
    from Jogo import Peca
    from Jogo import Carta
    from Jogo import Ataque

class Mesa():
    def __init__(self, jogadores, seed: int):    
        np.random.seed(seed)
        
        self.__turno: int = 0
        self.__fase: str = FaseTipo.INICIO
        self.__jogador_no_controle: Jogador = None
        self.__tokens_bloqueados: bool = False
        
        self.__tabuleiro = Tabuleiro()
        self.__pilha_cartas: list[Carta] = []
        self.__pilha_descarte: list[Carta] = []
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
        
        self.__saco_tokens = list(np.random.permutation(self.__saco_tokens))
        monstros_iniciais = list(np.random.permutation(monstros_iniciais))
        for fatia, monstro_inicial in enumerate(monstros_iniciais):
            self.__tabuleiro.colocar_peca(monstro_inicial, AnelTipo.FLORESTA, fatia)
        
        # Inicializa Cartas
        # 3 Red Archer
        self.__pilha_cartas += [Dano(CartaTipo.ARQUEIRO, FatiaCor.VERMELHO) for i in range(3)]
        # 3 Red Knight
        self.__pilha_cartas += [Dano(CartaTipo.CAVALEIRO, FatiaCor.VERMELHO) for i in range(3)]
        # 3 Red Swordsman
        self.__pilha_cartas += [Dano(CartaTipo.ESPADACHIM, FatiaCor.VERMELHO) for i in range(3)]
        # 3 Blue Archer
        self.__pilha_cartas += [Dano(CartaTipo.ARQUEIRO, FatiaCor.AZUL) for i in range(3)]
        # 3 Blue Knight
        self.__pilha_cartas += [Dano(CartaTipo.CAVALEIRO, FatiaCor.AZUL) for i in range(3)]
        # 3 Blue Swordsman
        self.__pilha_cartas += [Dano(CartaTipo.ESPADACHIM, FatiaCor.AZUL) for i in range(3)]
        # 3 Green Archer
        self.__pilha_cartas += [Dano(CartaTipo.ARQUEIRO, FatiaCor.VERDE) for i in range(3)]
        # 3 Green Knight
        self.__pilha_cartas += [Dano(CartaTipo.CAVALEIRO, FatiaCor.VERDE) for i in range(3)]
        # 3 Green Swordsman
        self.__pilha_cartas += [Dano(CartaTipo.ESPADACHIM, FatiaCor.VERDE) for i in range(3)]
        # 1 Any color Archer
        self.__pilha_cartas.append(Dano(CartaTipo.ARQUEIRO, FatiaCor.TODAS))
        # 1 Any color Knight
        self.__pilha_cartas.append(Dano(CartaTipo.CAVALEIRO, FatiaCor.TODAS))
        # 1 Any color Swordsman
        self.__pilha_cartas.append(Dano(CartaTipo.ESPADACHIM, FatiaCor.TODAS))
        # 1 Red Hero
        self.__pilha_cartas.append(Dano(CartaTipo.HEROI, FatiaCor.VERMELHO))
        # 1 Blue Hero
        self.__pilha_cartas.append(Dano(CartaTipo.HEROI, FatiaCor.AZUL))
        # 1 Green Hero
        self.__pilha_cartas.append(Dano(CartaTipo.HEROI, FatiaCor.VERDE))
        # 1 Barbarian
        self.__pilha_cartas.append(Barbaro())
        # 1 Drive Him Back!
        self.__pilha_cartas.append(Empurrao())
        # 1 Tar
        self.__pilha_cartas.append(Pixe())
        # 1 Draw 2 Cards
        self.__pilha_cartas.append(Comprar())
        # 1 Missing
        self.__pilha_cartas.append(Perdido())
        # 1 Nice Shot
        self.__pilha_cartas.append(BoaMira())
        # 1 Fortify Wall
        self.__pilha_cartas.append(Fortificar())
        # 1 Brick
        self.__pilha_cartas.append(ReparoMuro(CartaTipo.TIJOLO))
        # 1 Mortar
        self.__pilha_cartas.append(ReparoMuro(CartaTipo.MORTAR))
        
        self.__pilha_cartas = list(np.random.permutation(self.__pilha_cartas))
        
        
        # Inicializa Jogadores
        self.__jogadores: dict[Jogador] = {info[1]: Jogador(*info, mesa=self) for info in jogadores}
        
        self.__ordem_jogadores = list(self.__jogadores.values())
        self.__ordem_jogadores.sort(key=lambda x: x.ordem)
        self.__jogador_no_controle = self.__ordem_jogadores[0]
        
        for jogador in self.__ordem_jogadores:
            jogador.comprar_mao()
        
        
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
    def get_carta_id(self, carta: Carta):
        return self.__mao.index(carta)
        
    def get_carta_from_id(self, idx: int):
        return self.__mao[idx]

    @property
    def jogadores(self):
        return self.__jogadores

    @property
    def turno(self):
        return self.__turno
    
    @property
    def fase(self):
        return self.__fase

    def get_carta_compra(self) -> Carta:
        if len(self.__pilha_cartas) == 0:
            self.__pilha_cartas = list(np.random.permutation(self.__pilha_descarte))
            self.__pilha_descarte = []
            if len(self.__pilha_cartas) == 0:
                return None
        return self.__pilha_cartas.pop()

    def put_descarte(self, carta: Carta) -> None:
        self.__pilha_descarte.append(carta)

    def get_num_cartas(self) -> int:
        n_jogadores = len(self.__jogadores)
        if n_jogadores == 2:
            return 6
        elif n_jogadores <= 5:
            return 5
        else:
            return 4

    def get_turn(self) -> int:
        return self.__turno

    def get_tabuleiro(self) -> Tabuleiro:
        return self.__tabuleiro

    def passar_jogada(self, jogador_passante: Jogador) -> bool:
        # Guarda
        if jogador_passante != self.__jogador_no_controle:
            return False
        
        self.__fase = FaseTipo.PASSAGEM
        fim = False

        self.__tabuleiro.mover_montros(self)
        self.__tabuleiro.criar_tokens(self)
        destruidas = self.__tabuleiro.verificar_torres_destruidas()

        if destruidas:
            self.declarar_derrota()
            return True
        
        else:
            haMonstros = self.__tabuleiro.haMonstros()
            if not haMonstros:
                self.declarar_vitoria()
                return True
            else:
                self.proximo_jogador()
                self.__jogador_no_controle.comprar_mao()

        self.__tokens_bloqueados = False
        self.__fase = FaseTipo.INICIO
        self.__turno += 1
        return True


    def descartar_comprar(self, carta: Carta, jogador: Jogador) -> bool:
        if not jogador is self.__jogador_no_controle:
            return False

        if self.__fase > FaseTipo.DESCARTE:
            return False
        
        self.__fase = FaseTipo.DESCARTE
        if jogador is self.__jogador_no_controle:
            pertence: bool = jogador.descartar(carta)
            if pertence:
                jogador.comprar_carta()
                return True
        return False

    def selecionar_carta_descarte(self, carta: Carta, jogador: Jogador) -> bool:
        acao: Acao = jogador.get_acao_pendente()
        if acao.tipo == CartaTipo.RECICLAR:
            acao.agir(acao, jogador, None, None)
            return True
        return False

    def selecionar_monstro(self, monstro: Monstro, pos: Posicao, jogador: Jogador) -> bool:
        acao: Acao = jogador.get_acao_pendente()
        print("acao: ", str(acao))
        if isinstance(acao, Ataque):
            alcanca: bool = acao.verificar_alcance(pos)
            print("alcanca: ", alcanca)
            if alcanca:
                acao.agir(None, jogador, pos, monstro)
                return True
        return False

    def selecionar_posicao(self, pos: Posicao, jogador: Jogador) -> bool:
        acao: Acao = jogador.get_acao_pendente()
        if isinstance(acao, Fortificar) and pos.ha_muro() and not pos.ha_fortificacao():
            acao.agir(None, jogador, pos, None)
            return True
        elif isinstance(acao, ReparoMuro) and not pos.ha_muro():
            acao.agir(None, jogador, pos, None)
            return True
        return False

    def jogar_carta(self, carta: Carta, jogador: Jogador) -> bool:
        pertence = jogador.possui_carta(carta)
        
        if pertence and self.__jogador_no_controle == jogador:
            carta.ativar(jogador)
            self.__fase = FaseTipo.JOGADA
            return True
        return False

    def declarar_vitoria(self) -> None:
        self.__fase = FaseTipo.VITORIA

    def declarar_derrota(self) -> None:
        self.__fase = FaseTipo.DERROTA

    def proximo_jogador(self) -> None:
        atual = self.__jogador_no_controle
        atual.encerra_turno()
        if self.__ordem_jogadores[-1] == atual:
            self.__jogador_no_controle = self.__ordem_jogadores[0]
        else:
            self.__jogador_no_controle = self.__ordem_jogadores[atual.ordem]

    def descartar_todas(self, carta_tipo: CartaTipo) -> None:
        for jogador in self.__jogadores.values():
            jogador.descartar_todas(carta_tipo)

    def todos_descartam_um(self) -> None:
        for jogador in self.__jogadores.values():
            jogador.descartar_aleatoria()

    def bloquear_tokens(self) -> None:
        self.__tokens_bloqueados = True

    def colocar_peca(self, peca: Peca, anel: int, fatia: int) -> None:
        self.__tabuleiro.colocar_peca(peca, anel, fatia)

    def get_token(self) -> Token:
        if self.__tokens_bloqueados or not len(self.__saco_tokens):
            return None
        return self.__saco_tokens.pop()
    
    @property
    def jogador_no_controle(self) -> Jogador:
        return self.__jogador_no_controle
