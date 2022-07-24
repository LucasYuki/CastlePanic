from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from .ImageHelper import ImageHelper

class InfoViewer(Canvas):
    __slots__ = ("__layout", "__text_space", "__text_idx", "__zoom_idx",
                 "__zoom_img", "__zoom_img_tk")
    
    def __init__(self, layout, borderwidth=0, highlightthickness=0 ,**kwargs):
        self.__layout = layout
        Canvas.__init__(self, layout, borderwidth=borderwidth,
                        highlightthickness=highlightthickness, **kwargs)

        self.__text_space = 45
        
        self.__text_idx = self.create_text(self.__layout.padding, self.__layout.padding,
                                       text='Zoom and other UI elements', anchor='nw')
        
        self.__zoom_idx = self.create_image(
            self.__layout.padding, self.__text_space+self.__layout.padding*2,
            image=None, anchor='nw')
        self.__zoom_img = None
        self.__zoom_img_tk = None

        self.bind("<Configure>", self.__on_resize)
    
    def __on_resize(self, event):
        if self.__zoom_img is None:
            return
        self.__resize_img()

    def __resize_img(self):
        max_width = self.winfo_width()-self.__layout.padding*2
        height = self.winfo_height()-self.__layout.padding*3-self.__text_space
        self.__zoom_img_tk = ImageHelper.get_tk_image(
            self.__zoom_img, height=height, max_width=max_width)
        self.itemconfig(self.__zoom_idx, image=self.__zoom_img_tk)

    def zoom(self, img: ImageTk.PhotoImage):
        self.__zoom_img = img
        self.__resize_img()
    
    def set_info(self, txt: str):
        self.itemconfig(self.__text_idx, text=txt)
