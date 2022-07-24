from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import Interface
from Distribuido import CastlePanicDistribuido

class PlayerInterface(Tk):
    __slots__ = "__frames", "__jogo"

    def __init__(self):
        super().__init__()
        self.title("Castle Panic")
        self.__jogo = CastlePanicDistribuido(self)

        self.__frames = {}
        self.__frames["menu"] = Interface.Menu(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.__set_frame("menu")
        self.maximize_window()

        self.mainloop()

    def __set_frame(self, frame_name: str):
        self.__frames[frame_name].tkraise()

    def maximize_window(self):
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
    
    def start_game(self, n_players: int, player_name: str):
        message = self.__jogo.initialize(player_name)
        if message == "Conectado a Dog Server":
            self.__frames["menu"].set_info(message+". Esperando Inicio da partida...")
        else:
            txt = "Não foi possível iniciar o jogo (%s). Tente novamente." %message
            self.__frames["menu"].set_info(txt)
            return
    
        code, message = self.__jogo.start_match(n_players)
        if code == "1":
            txt = "Jogadores insuficientes. Aguarde incio da partida... (quantidade de jogadores aleatória)"
            self.__frames["menu"].set_info(txt)
        elif code == 0:
            txt = "Não foi possível iniciar o jogo (%s). Tente novamente." %message
            self.__frames["menu"].set_info(txt)
    
    def proceed_start(self, start_function):
        txt = "Iniciando jogo..."
        self.__frames["menu"].set_info(txt)
        
        start_function()
        
        if not "game" in self.__frames:
            self.__frames["game"] = Interface.LayoutGame(self, self.__jogo)
        print("Trocando Frame")
        self.__set_frame("game")
        print("Frame Trocado")
