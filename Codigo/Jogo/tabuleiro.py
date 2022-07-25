from __future__ import annotations
from typing import TYPE_CHECKING

from .enums import AnelTipo
from .fatia import Fatia
from .peca import Torre, Muro
from .monstro import Monstro
if TYPE_CHECKING:  # importa classes abaixo apenas para verificar tipos
    from Jogo import Monstro
    from Jogo import Posicao
    from Jogo import Mesa
    from Jogo import Token
    from Jogo import Peca

class Tabuleiro:
    def __init__(self):
        self.__fatias: list[Fatia] = []
        for i in range(1, 7):
            self.__fatias.append(Fatia(i))
            self.__fatias[-1].colocar_peca(Torre(), AnelTipo.CASTELO)
            self.__fatias[-1].colocar_peca(Muro(), AnelTipo.CASTELO)
            
    def colocar_peca(self, peca: Peca, anel: AnelTipo, fatia: int) -> None:
        self.__fatias[fatia].colocar_peca(peca, anel)

    def verificar_torres_destruidas(self) -> bool:
        for fatia in self.__fatias:
            if not fatia.verificar_torres_destruidas():
                return False
        return True

    def haMonstros(self) -> bool:
        for fatia in self.__fatias:
            if fatia.haMonstros():
                return True
        return False

    def criar_tokens(self, mesa: Mesa) -> None:
        for _ in range(2):
            self.novo_token(mesa)

    def mover_montros(self, mesa: Mesa) -> None:
        pecas_dict: dict = self.get_pecas_dict()
        
        while pecas_dict != {}:
            origem, pecas = pecas_dict.popitem()

            monstros = list(filter(lambda p: isinstance(p, Monstro), pecas))
            if monstros == []:
                continue

            destino: Posicao = self.determinar_posicao_destino(origem)
            ha_construcao: bool = destino.ha_construcao()
            if not ha_construcao:
                self.mover_monstros_para_destino(monstros, origem, destino, mesa)
            else:
                morto: bool = monstros[0].danificar()
                destino.destruir_construcao()
                if morto:
                    origem.remover_monstro(monstros[0])
            

    def get_pecas_dict(self) -> dict:
        pecas_dict = {}
        for fatia in self.__fatias:
            for posicao in fatia.aneis.values():
                if len(posicao.pecas) != 0:
                    pecas_dict[posicao] = posicao.pecas
        return pecas_dict

    def determinar_posicao_destino(self, origem: Posicao) -> Posicao:
        anel, fatia = origem.get_anel_fatia()
        if anel == 4: # castelo
            fatia_destino = self.get_fatia(fatia+1)
            destino = fatia_destino.get_posicao(anel)
        else:
            fatia_origem = self.get_fatia(fatia)
            destino = fatia_origem.get_posicao(anel + 1)
        return destino

    def mover_monstros_para_destino(self, monstros: list, origem: Posicao, destino: Posicao, mesa: Mesa) -> None:
        for monstro in monstros:
            if not monstro.imovel(mesa.turno):
                origem.remover_monstro(monstro)
                destino.colocar_peca(monstro)

    def novo_token(self, mesa: Mesa) -> None:
        token = mesa.get_token()
        if token:
            token.invocar(mesa)

    def pedra(self, fatia: Fatia) -> None:
        atravessou: bool = fatia.pedra_entrando()
        if atravessou:
            self.get_fatia(fatia.num + 3).pedra_saindo()

    def curar_todos(self) -> None:
        for fatia in self.__fatias:
            fatia.curar_todos()
            
    def get_fatia(self, fatia: int) -> Fatia:
        return self.__fatias[(fatia-1) % 6]