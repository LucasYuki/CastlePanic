from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from .ImageHelper import ImageHelper

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
        self.bind("<Button-1>", self.__on_click)
        self.bind("<Motion>", self.__on_hover)
        
        #Apenas para demonstrar que os efeitos de hover e click estão funcionando
        self.oval = None
        self.pointer = None
        
        self.bind("<Configure>", self.__on_resize)
    
    def __on_resize(self, event):
        self.__img_tk = ImageHelper.get_tk_image(self.__img_orig, event.width, event.height)
        self.itemconfig(self.__img_idx, image=self.__img_tk)

    def __on_click(self, event):
        if self.oval is not None:
            self.delete(self.oval)
        self.oval = self.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red', outline='blue')
        self.__layout.set_info("Click on (%i, %i)" %(event.x, event.y))

    def __on_hover(self, event):
        if self.pointer is None:
            self.pointer = self.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill='blue', outline='red')
        else:
            self.coords(self.pointer, event.x-5, event.y-5, event.x+5, event.y+5)
    
    def update(self):
        pecas_dict = board.get_pecas_dict()
        for posicao, pecas in pecas_dict.items():
            #colocar as pecas igual cartas no outro bagulho
    
    @property
    def aspect_ratio(self):
        return self.__aspect_ratio