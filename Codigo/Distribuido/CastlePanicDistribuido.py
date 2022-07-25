from DOG import DogPlayerInterface, DogActor, StartStatus
from Jogo import Mesa, FaseTipo, AcaoJogadorTipo, Carta, Monstro, Posicao
import time 

class CastlePanicDistribuido(DogPlayerInterface):
    def __init__(self, gui):
        self.__gui = gui
        super().__init__()
        self.__jogo = None
        self.__conected = False
        self._dog_server_interface = DogActor()
    
    @staticmethod
    def concat_seed(name):
        return "/".join([str(time.time_ns()), name])
    
    @staticmethod
    def extract_seed(players: list) -> (list, int):
        seed = 0
        for i in range(len(players)):
            player_seed, player_name = players[i][0].split("/", 1)
            players[i][0] = player_name
            seed += int(player_seed)
        return players, seed % (2**32 - 1)

    def initialize(self, player_name: str):
        if not self.__conected:
            seed_name = self.concat_seed(player_name)
            message = self._dog_server_interface.initialize(seed_name, self)
            if message == "Conectado a Dog Server":
                self.__conected = True
            return message
        else:
            return "Conectado a Dog Server"

    def start_match(self, n_players: int):
        start_status = self._dog_server_interface.start_match(n_players)
        code = start_status.get_code()
        message = start_status.get_message()
        if code == "2":
            self.receive_start(start_status)
        elif code == "0":
            self.__conected = False
        return code, message

    def receive_start(self, start_status: StartStatus):
        players = start_status.get_players()
        idx = start_status.get_local_id()
        self.__gui.proceed_start(lambda : self.proceed_start(players, idx))
    
    def proceed_start(self, players: list, local_player_id: str):
        print("starting game")
        print()
        self.__local_player_id = local_player_id
        players, seed = self.extract_seed(players)
        print(seed)
        print(players)
        self.__jogo = Mesa(players, seed=seed)
        self.__local_player = self.__jogo.jogadores[self.__local_player_id]

    def receive_move(self, a_move: dict):
        tipo = a_move["Action"]
        player = self.__jogo.jogadores[a_move["player"]]
        if tipo == AcaoJogadorTipo.DESCARTAR:
            carta = player.get_carta_from_id(a_move["carta_idx"])
            sucesso = self.__jogo.descartar_comprar(carta, player)
        elif tipo == AcaoJogadorTipo.JOGAR:
            carta = player.get_carta_from_id(a_move["carta_idx"])
            sucesso = self.__jogo.jogar_carta(carta, player)
        elif tipo == AcaoJogadorTipo.SELECIONAR_DESCARTE:
            carta = player.get_carta_from_id(a_move["carta_idx"])
            sucesso = self.__jogo.selecionar_carta_descarte(carta, player)
        elif tipo == AcaoJogadorTipo.SELECIONAR_MONSTRO:
            posicao = self.__jogo.get_tabuleiro().get_fatia(a_move["posicao"]["fatia"]).get_posicao(a_move["posicao"]["anel"])
            print(posicao)
            monstro = posicao.get_peca_from_id(a_move["monstro_idx"])
            sucesso = self.__jogo.selecionar_monstro(monstro, posicao, player)
        elif tipo == AcaoJogadorTipo.SELECIONAR_POSICAO:
            posicao = self.__jogo.get_tabuleiro().get_fatia(a_move["posicao"]["fatia"]).get_posicao(a_move["posicao"]["anel"])
            sucesso = self.__jogo.selecionar_posicao(posicao, player)
        elif tipo == AcaoJogadorTipo.PASSAR:
            sucesso = self.__jogo.passar_jogada(player)
            
        if sucesso:
            self.__gui.update()

    def receive_withdrawal_notification(self):
        pass #???
    
    @property
    def conected(self):
        return self.__conected

    @property
    def jogadores(self):
        if self.__jogo is not None:
            return self.__jogo.jogadores
        else:
            return None
        
    def descartar_comprar(self, carta : Carta):
        if self.__jogo.jogador_no_controle == self.__local_player:
            carta_idx = self.__jogo.jogadores[self.__local_player_id].get_carta_id(carta)
            move_info = {"carta_idx": carta_idx}
            
            sucesso = self.__jogo.descartar_comprar(carta, self.__local_player)
            print("CastlePanicDistribuido descartar_comprar", sucesso)
            if sucesso:
                self.send_move(AcaoJogadorTipo.DESCARTAR, "progress", move_info)
            return sucesso
        return False
    
    def jogar_carta(self, carta : Carta):
        if self.__jogo.jogador_no_controle == self.__local_player:
            carta_idx = self.__jogo.jogadores[self.__local_player_id].get_carta_id(carta)
            move_info = {"carta_idx": carta_idx}
            
            sucesso = self.__jogo.jogar_carta(carta, self.__local_player)
            print("CastlePanicDistribuido jogar_carta", sucesso)
            if sucesso:
                self.__gui.update()
                self.send_move(AcaoJogadorTipo.JOGAR, "progress", move_info)
            return sucesso
        return False
        
    def selecionar_carta_descarte(self, carta : Carta):
        if self.__jogo.jogador_no_controle == self.__local_player:
            carta_idx = self.__jogo.jogadores[self.__local_player_id].get_carta_id(carta)
            move_info = {"carta_idx": carta_idx}
            
            sucesso = self.__jogo.selecionar_carta_descarte(carta, self.__local_player)
            print("CastlePanicDistribuido selecionar_carta_descarte", sucesso)
            if sucesso:
                self.__gui.update()
                self.send_move(AcaoJogadorTipo.SELECIONAR_DESCARTE, "progress", move_info)
            return sucesso
        return False
    
    def selecionar_monstro(self, monstro: Monstro, posicao: Posicao):
        if self.__jogo.jogador_no_controle == self.__local_player:
            move_info = {"posicao": posicao.get_info_dict(), 
                         "monstro_idx": posicao.get_peca_id(monstro)}
            
            sucesso = self.__jogo.selecionar_monstro(monstro, posicao, self.__local_player)
            print(posicao)
            print(move_info)
            print("CastlePanicDistribuido selecionar_monstro", sucesso)
            if sucesso:
                self.__gui.update()
                self.send_move(AcaoJogadorTipo.SELECIONAR_MONSTRO, "progress", move_info)
            return sucesso
        return False
    
    def selecionar_posicao(self, posicao: Posicao):
        if self.__jogo.jogador_no_controle == self.__local_player:
            move_info = {"posicao": posicao.get_info_dict()}
            sucesso = self.__jogo.selecionar_posicao(posicao, self.__local_player)
            print("CastlePanicDistribuido selecionar_posicao", sucesso)
            if sucesso:
                self.__gui.update()
                self.send_move(AcaoJogadorTipo.SELECIONAR_POSICAO, "progress", move_info)
            return sucesso
        return False
    
    def passar_jogada(self):
        sucesso = self.__jogo.passar_jogada(self.__local_player)
        print("CastlePanicDistribuido passar_jogada", sucesso)
        if sucesso:
            self.__gui.update()
            self.send_move(AcaoJogadorTipo.PASSAR, "progress", {})
        return sucesso
    
    def send_move(self, action: AcaoJogadorTipo, match_status, move_info: dict):
        move_info["Action"] = action
        move_info["match_status"] = "progress"
        move_info["player"] = self.__local_player_id
        self._dog_server_interface.send_move(move_info)
    
    def get_tabuleiro(self):
        return self.__jogo.get_tabuleiro()
    
    def get_mesa(self):
        return self.__jogo
    
    def get_fase(self) -> FaseTipo:
        return self.__jogo.fase