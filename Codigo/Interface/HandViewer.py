from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from .ImageHelper import ImageHelper
from Jogo import Carta

class HandViewer(Canvas):
    __slots__ = "__layout", "__player_hand", "__imgs", "__cards_idx", \
        "__current_width", "__current_height", "__jogador"
    
    def __init__(self, layout, jogador, borderwidth=0,
                 highlightthickness=0, **kwargs):
        self.__jogador = jogador
        self.__layout = layout
        Canvas.__init__(self, self.__layout, borderwidth=borderwidth, 
                        highlightthickness=highlightthickness, **kwargs)
        self.__current_width = 1
        self.__current_height = 1
        
        self.update()
        self.bind("<Configure>", self.__on_resize)
    
    def update(self):
        self.__player_hand = self.__jogador.get_mao()

        self.__cards_idx = []
        self.__imgs = []
        for i in range(len(self.__player_hand)):
            self.__imgs.append(ImageTk.PhotoImage(self.__player_hand[i].imagem))
            self.__cards_idx.append(self.create_image(0, 0, image=self.__imgs[i], 
                                                anchor='nw'))
            self.tag_bind(self.__cards_idx[i], "<Enter>",
                          lambda e, idx=i: self.__on_hover(e, idx))
            self.tag_bind(self.__cards_idx[i], "<Button-1>",
                          lambda e, idx=i: self.__on_click(e, idx))
    
    def __on_resize(self, event):
        self.__current_width = event.width-self.__layout.padding*2
        self.__current_height = event.height-self.__layout.padding*2
        self.__resize()
        
    def __resize(self):
        n_cards = len(self.__cards_idx)
        if n_cards==0:
            return
        card_height = self.__current_height
        card_width = card_height*Carta.ratio()
        space = self.__current_width-card_width
        
        card_size = (int(card_width), card_height)
        for i in range(n_cards):
            self.__imgs[i] = ImageHelper.get_tk_image(self.__player_hand[i].imagem, *card_size)
            self.itemconfig(self.__cards_idx[i], image=self.__imgs[i]) 
            self.coords(self.__cards_idx[i], (self.__layout.padding+(i*space)//(n_cards-1),
                                          self.__layout.padding))
    
    def __on_hover(self, event, idx: int):
        self.__layout.zoom(self.__player_hand[idx].imagem)

    def __on_click(self, event, idx: int):
        self.__layout.set_info("Click on card %i" %(idx))
