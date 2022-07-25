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
        self.__current_width = 100
        self.__current_height = 100
        
        self.update()
        self.bind("<Configure>", self.__on_resize)
    
    def update(self):
        self.__selected = None
        self.__player_hand = self.__jogador.get_mao()

        self.__cards_idx = {}
        self.__imgs = {}
        for carta in self.__player_hand:
            self.__imgs[carta] = ImageTk.PhotoImage(carta.imagem)
            idx = self.create_image(0, 0, image=self.__imgs[carta], anchor='nw')
            self.__cards_idx[carta] = idx
            self.tag_bind(idx, "<Enter>", lambda e, c=carta: self.__on_hover(e, c))
            self.tag_bind(idx, "<Button-1>", lambda e, c=carta: self.__on_click(e, c))
        self.__resize()
    
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
        for i, carta in enumerate(self.__player_hand):
            self.__imgs[carta] = ImageHelper.get_tk_image(carta.imagem, *card_size)
            self.itemconfig(self.__cards_idx[carta], image=self.__imgs[carta]) 
            self.coords(self.__cards_idx[carta], (self.__layout.padding+(i*space)//max(n_cards-1, 1),
                                          self.__layout.padding))
    
    def __on_hover(self, event, carta: Carta):
        self.__layout.zoom(carta.imagem)

    def __on_click(self, event, carta: Carta):
        self.__layout.set_info("Carta %s selecionada" %str(carta.tipo))
        self.__selected = carta

    @property
    def selected(self):
        return self.__selected