from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from .ImageHelper import ImageHelper
import numpy as np
from Jogo import Peca, Posicao, Construcao, Monstro, Muro, Fortificacao

class BoardView(Canvas):
    __slots__ = ("__layout", "__aspect_ratio", "__img_orig", "__img_tk",
                 "__img_idx")

    def __init__(self, layout, board, width=800, height=800,
                 borderwidth=0, highlightthickness=0, **kwargs):
        self.__layout = layout
        Canvas.__init__(self, layout, borderwidth=borderwidth, 
                        highlightthickness=highlightthickness, 
                        width=width, height=height, **kwargs)
        
        self.__board = board
        self.__aspect_ratio = width/height
        self.__img_orig = Image.open('Images/base/Tabuleiro.jpg')
        self.__img_tk = ImageHelper.get_tk_image(self.__img_orig, width, height)
        self.__img_idx = self.create_image(0, 0, image=self.__img_tk, anchor='nw')
        self.__current_width = width
        self.__current_height = height
        
        self.update()
        self.bind("<Configure>", self.__on_resize)
    
    def update(self):
        self.__pecas_dict = self.__board.get_pecas_dict()
        self.__peca_idx = {}
        self.__imgs = {}
        self.__rotation = {}
        for posicao, pecas in self.__pecas_dict.items():
            for peca in pecas:
                self.__rotation[peca] = BoardView.get_rotation(posicao, peca)
                self.__imgs[peca] = ImageTk.PhotoImage(peca.get_image())
                self.__peca_idx[peca] = self.create_image(0, 0, image=self.__imgs[peca], 
                                                          anchor='nw')
                #self.tag_bind(self.__peca_idx[i], "<Enter>",
                #              lambda e, idx=i: self.__on_hover(e, idx))
                self.tag_bind(self.__peca_idx[peca], "<Button-1>",
                              lambda e, p=peca: self.__on_click(e, p))
        self.__resize()
    
    def __on_resize(self, event):
        self.__current_width = event.width
        self.__current_height = event.height
        self.__img_tk = ImageHelper.get_tk_image(self.__img_orig, event.width, event.height)
        self.itemconfig(self.__img_idx, image=self.__img_tk)
        self.__resize()
    
    def __resize(self):
        size = (self.__current_width//15, self.__current_height//15)
        for posicao, pecas in self.__pecas_dict.items():
            n_pecas = len(pecas)
            if posicao.ha_fortificacao():
                n_pecas -= 2
            elif posicao.ha_muro():
                n_pecas -= 1
            initial_angle = ((60*3 - posicao.fatia*60) % 360)
            radius = self.__current_width/2/5 * (4.5 - posicao.anel.value)
            fortificacao = None
            i = 0
            for peca in pecas:
                rotated_image = peca.get_image().rotate(self.__rotation[peca])
                self.__imgs[peca] = ImageHelper.get_tk_image(rotated_image, *size)
                self.itemconfig(self.__peca_idx[peca], image=self.__imgs[peca]) 
                
                if isinstance(peca, Muro):
                    angle = initial_angle + 30
                    x = self.__current_width/2 + np.sin(angle*np.pi/180)*radius*2 - size[0]/2
                    y = self.__current_height/2 + np.cos(angle*np.pi/180)*radius*2 - size[1]/2
                    self.coords(self.__peca_idx[peca], (int(x), int(y)))
                elif isinstance(peca, Fortificacao):
                    fortificacao = peca # desenha por último
                else:
                    angle = initial_angle + 60/n_pecas*(i+0.5)
                    x = self.__current_width/2 + np.sin(angle*np.pi/180)*radius - size[0]/2
                    y = self.__current_height/2 + np.cos(angle*np.pi/180)*radius - size[1]/2
                    i += 1
                    self.coords(self.__peca_idx[peca], (int(x), int(y)))
            if fortificacao is not None:
                angle = initial_angle + 30
                x = self.__current_width/2 + np.sin(angle*np.pi/180)*radius*1.1 - size[0]/2
                y = self.__current_height/2 + np.cos(angle*np.pi/180)*radius*1.1 - size[1]/2
                self.coords(self.__peca_idx[fortificacao], (int(x), int(y)))

    def __on_click(self, event, peca: Peca):
        print("aaa aaaaaaaaaaa")
        print("Click on ", self.__peca_idx[peca])

    @property
    def aspect_ratio(self):
        print("__aspect_ratio =", self.__aspect_ratio)
        return self.__aspect_ratio
    
    @staticmethod
    def get_rotation(posicao: Posicao, peca: Peca):
        if isinstance(peca, Construcao):
            return (30+60*3 - posicao.fatia*60) % 360
        elif isinstance(peca, Monstro):
            return (30+60*3 - posicao.fatia*60 + 180 - peca.vida_perdida()) % 360
        else:
            raise ValueError("peca deve ser monstro ou construção")
            
        