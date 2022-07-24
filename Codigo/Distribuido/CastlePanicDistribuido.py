from DOG import DogPlayerInterface, DogActor, StartStatus
from Jogo import Mesa
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

    @property
    def conected(self):
        return self.__conected

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
        self.__jogo = Mesa(players, seed=seed)

    def receive_move(self, a_move: dict):
        print(a_move)

    def receive_withdrawal_notification(self):
        pass #???
    
    @property
    def jogadores(self):
        if self.__jogo is not None:
            return self.__jogo.jogadores
        else:
            return None
    
    def send_move(self, action, match_status, **move_info):
        move_info["Action"] = action
        move_info["match_status"] = "progress"
        self._dog_server_interface.send_move(move_info)
    
    def get_tabuleiro(self):
        return self.__jogo.get_tabuleiro()