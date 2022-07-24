# -*- coding: utf-8 -*-
from enum import IntEnum, unique, auto

class IterEnum(IntEnum):
    @staticmethod
    def list(reverse=False, key=None):
        member_list = list(AnelTipo)
        member_list.sort(reverse=reverse, key=key)
        return member_list

@unique
class AnelTipo(IterEnum):
    FLORESTA = 0,
    ARQUEIRO = 1,
    CAVALEIRO = 2,
    ESPADACHIM = 3,
    CASTELO = 4

@unique
class FatiaCor(IterEnum):
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
