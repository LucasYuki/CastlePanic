from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw
import Interface

class Menu(ttk.Frame):
    __slots__ = "__n_players", "__n_min_players", "__n_max_players", "__player_name_box", \
        "__interface", "__n_players_lbl"
    
    def __init__(self, interface, **kwargs):
        self.__interface = interface
        super().__init__(self.__interface, **kwargs)
        
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        main_frame = ttk.Frame(self)
        main_frame.grid(column=1, row=1, sticky=(N, S, E, W))
        self.rowconfigure((0, 2), weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure((0, 2), weight=2)
        self.columnconfigure(1, weight=1)
        
        title_lbl = Label(main_frame, text="Castle Panic")
        title_lbl.grid(column=0, row=0, columnspan=4, sticky=(N, S, E, W))
        
        lbl = Label(main_frame, text="Nome do Jogador: ")
        lbl.grid(column=0, row=1, sticky=(N, S, E, W))
        self.__player_name_box = Entry(main_frame, width=15)
        self.__player_name_box.insert(0, "Jogador")
        self.__player_name_box.grid(column=1, row=1, columnspan=3, sticky=(N, S, E, W))
        
        self.__n_players = 2
        self.__n_min_players = 2
        self.__n_max_players = 6
        
        start_button = Button(main_frame, text="Iniciar", command=self.start_game)
        start_button.grid(column=0, row=2, sticky=(N, S, E, W))
        
        n_players_dec = Button(main_frame, text="-", command=self.dec_players)
        n_players_dec.grid(column=1, row=2, sticky=(N, S, E))
        self.__n_players_lbl = Label(main_frame, text="Nº Jogadores: %i" %self.__n_players)
        self.__n_players_lbl.grid(column=2, row=2, sticky=(N, S, E, W))
        n_players_inc = Button(main_frame, text="+", command=self.inc_players)
        n_players_inc.grid(column=3, row=2, sticky=(N, S, W))
        
        self.__info = Label(main_frame, text=self.default_info)
        self.__info.grid(column=0, row=3, columnspan=4, sticky=(N, S, E, W))
        
        main_frame.rowconfigure((0, 1, 2, 3), weight=1)
        main_frame.columnconfigure((0, 1, 2, 3), weight=1)

    @property
    def default_info(self):
        return "Selecione a quantidade de jogadores, coloque seu nome e clique em Iniciar."
    
    def dec_players(self):
        if self.__n_players == self.__n_min_players:
            self.__n_players = self.__n_max_players
        else:
            self.__n_players -= 1
        self.__n_players_lbl.configure(text="Nº Jogadores: %i" %self.__n_players)
    
    def inc_players(self):
        if self.__n_players == self.__n_max_players:
            self.__n_players = self.__n_min_players
        else:
            self.__n_players += 1
        self.__n_players_lbl.configure(text="Nº Jogadores: %i" %self.__n_players)
    
    def start_game(self):
        self.set_info("Tentando conectar com o servidor...")
        self.__interface.start_game(self.__n_players, self.__player_name_box.get())
    
    def set_info(self, txt: str):
        self.__info.configure(text=txt)