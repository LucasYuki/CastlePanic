# -*- coding: utf-8 -*-
from enum import IntEnum, unique, auto

class IterEnum(IntEnum):    
    @classmethod
    def list(cls, reverse=False):
        member_list = list(cls)
        member_list.sort(reverse=reverse)
        return member_list

@unique
class AcaoJogadorTipo(IterEnum):
    DESCARTAR = 0,
    JOGAR = 1,
    SELECIONAR_TOKEN = 2,
    SELECIONAR_POSICAO = 3,
    SELECIONAR_DESCARTE = 4,
    PASSAR = 5

@unique
class FaseTipo(IterEnum):
    PASSAGEM = 0,
    INICIO = 1,
    DESCARTE = 2,
    JOGADA = 3,
    VITORIA = 4,
    DERROTA = 5

@unique
class AnelTipo(IterEnum):
    FLORESTA = 0,
    ARQUEIRO = 1,
    CAVALEIRO = 2,
    ESPADACHIM = 3,
    CASTELO = 4

@unique
class FatiaCor(IterEnum):
    TODAS = -1,
    VERMELHO = 0,
    VERDE = 1,
    AZUL = 2
    
    @staticmethod
    def num2cor(num: int):
        if num==1 or num==2:
            return FatiaCor.VERMELHO
        elif num==3 or num==4:
            return FatiaCor.VERDE
        elif num==5 or num==6:
            return FatiaCor.AZUL
        else:
            raise ValueError("num(%s) deve ser um inteiro entre 1 e 6" %str(num))

    @classmethod
    def list(cls, reverse=False, incluir_todas=False):
        member_list = super().list(reverse=False)
        if not incluir_todas:
            member_list.remove(cls.TODAS)
        return member_list

@unique
class ContrucaoTipo(IntEnum):
    TORRE = 1,
    MURO = 2,
    FORTIFICACAO = 3

@unique
class CartaTipo(IntEnum):
    ARQUEIRO = 1,
    CAVALEIRO = 2,
    ESPADACHIM = 3,
    HEROI = 4,
    BARBARO = 5,
    EMPURRAO = 6,
    PIXE = 7,
    PERDIDO = 8,
    FORTIFICAR = 9,
    RECICLAR = 10,
    BOAMIRA = 11,
    TIJOLO = 12,
    MORTAR = 13,
    COMPRAR = 14

@unique
class TokenTipo(IntEnum):
    GOBLIN = 1,
    ORC = 2,
    TROLL = 3,
    REI = 4,
    MAGO = 5,
    MEDICO = 6,
    AZUL_MOVE = 7,
    VERDE_MOVE = 8,
    VERMELHO_MOVE = 9,
    PRAGA_ESPADACHIM = 10,
    PRAGA_CAVALEIRO = 11,
    PRAGA_ARQUEIROS = 12,
    DESCARTA = 13,
    PEDRA = 14,
    COMPRAR_TOKEN_3 = 15,
    COMPRAR_TOKEN_4 = 16
    
    @staticmethod
    def is_monstro_normal(tipo: IntEnum):
        return tipo in (TokenTipo.GOBLIN, TokenTipo.ORC, TokenTipo.TROLL)
    
    @staticmethod
    def is_monstro_especial(tipo: IntEnum):
        return tipo in (TokenTipo.REI, TokenTipo.MAGO, TokenTipo.MEDICO)
    
    @staticmethod
    def is_monstro(tipo: IntEnum):
        return TokenTipo.is_monstro_normal(tipo) or TokenTipo.is_monstro_especial(tipo)
