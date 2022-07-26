from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import Interface
from Distribuido import CastlePanicDistribuido
from Jogo import Carta, Monstro, Posicao

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
        
    def return_to_menu(self):
        del self.__jogo
        self.__jogo = CastlePanicDistribuido(self)
        self.__frames["menu"].tkraise()
        del self.__frames["game"]

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
        self.__frames["game"].update()
        
    def update(self):
        self.__frames["game"].update()
    
    def descartar_comprar(self, carta : Carta):
        print("Interface descartar_comprar")
        if self.__jogo.descartar_comprar(carta):
            self.update()
    
    def jogar_carta(self, carta : Carta):
        print("Interface jogar_carta")
        if self.__jogo.jogar_carta(carta):
            self.update()

    def selecionar_carta_descarte(self, carta : Carta):
        print("Interface selecionar_carta_descarte")
        if self.__jogo.selecionar_carta_descarte(carta):
            self.update()
    
    def selecionar_monstro(self, monstro: Monstro, posicao: Posicao):
        print("Interface selecionar_monstro")
        if self.__jogo.selecionar_monstro(monstro, posicao):
            self.update()
    
    def selecionar_posicao(self, posicao: Posicao):
        print("Interface selecionar_posicao")
        if self.__jogo.selecionar_posicao(posicao):
            self.update()
    
    def passar_jogada(self):
        print("Interface passar_jogada")
        if self.__jogo.passar_jogada():
            self.update()
