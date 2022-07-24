from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw
import Interface
from Distribuido import CastlePanicDistribuido

class LayoutGame(ttk.Frame):
    __slots__ = ("__board", "__info", "__hands", "__hand_notebook", "__buttons",
        "__cancel_btn", "__play_btn", "__next_btn", "__padding", "__buttons_height")

    def __init__(self, interface, jogo: CastlePanicDistribuido, **kwargs):
        self.__jogo = jogo
        super().__init__(interface, **kwargs)
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        self.bind("<Configure>", self.__on_resize)
        
        self.__padding = 5
        self.__buttons_height = 25
        
        self.__board = Interface.BoardView(self, jogo.get_tabuleiro())
        self.__info = Interface.InfoViewer(self, background="bisque")

        self.__hand_notebook = ttk.Notebook(self) 
        self.__hands = []
        for jogador in self.__jogo.jogadores.values():
            hand = Interface.HandViewer(self, background="bisque",
                                        jogador=jogador)
            self.__hands.append(hand)
            self.__hand_notebook.add(hand, text=jogador.nome + " (%s)" %jogador.ordem)
        self.__current_player = 0
        self.__hand_notebook.select(self.__hands[self.__current_player])
        
        # Inicialização dos Botões                
        self.__buttons = ttk.Frame(self)
        self.__buttons.rowconfigure(0, weight=1)
        
        self.__cancel_btn = ttk.Button(self.__buttons, text="Cancel", command=self.cancel)
        self.__cancel_btn.grid(column=0, row=0, sticky=(N, W, E, S))
        self.__buttons.columnconfigure(0, weight=1)

        self.__play_btn = ttk.Button(self.__buttons, text="Play", command=self.play)
        self.__play_btn.grid(column=1, row=0, sticky=(N, W, E, S))
        self.__buttons.columnconfigure(1, weight=1)
        
        self.__next_btn = ttk.Button(self.__buttons, text="Pass", command=self.next_phase)
        self.__next_btn.grid(column=2, row=0, sticky=(N, W, E, S))
        self.__buttons.columnconfigure(2, weight=1)

    def __on_resize(self, event):
        #   Calcula a posição de cada uma das partes do layout quando o tamanho 
        # da janela é alterado
        width = event.width-self.__padding*2
        height = event.height-self.__padding*2
        proportion = width/height

        # Tamanho desejado do tabuleiro
        desired_height = height
        desired_width = int(height * self.__board.aspect_ratio)

        self.__board.place(
            in_=self,
            x=self.__padding+width-desired_width,
            y=self.__padding, 
            width=desired_width,
            height=desired_height)

        # Calcula o resto das posições no espaço que restou
        remaining_width = width - self.__padding - desired_width
        remaining_height = height-self.__padding*2-self.__buttons_height
        info_height = (remaining_height*2)//3
        hand_height = remaining_height-info_height

        self.__info.place(
            in_=self, 
            x=self.__padding, 
            y=self.__padding, 
            width=remaining_width,
            height=info_height)

        self.__hand_notebook.place(
            in_=self, 
            x=self.__padding, 
            y=self.__padding*2+info_height,
            width=remaining_width,
            height=hand_height)
        
        self.__buttons.place(
            in_=self,
            x=self.__padding,
            y=self.__padding*3+remaining_height, 
            width=remaining_width,
            height=self.__buttons_height)

    def cancel(self):
        self.__jogo.send_move("Cancel")
        self.set_info("Cancel")

    def play(self):
        self.__jogo.send_move("Play")
        self.set_info("Play")

    def next_phase(self):
        self.__jogo.send_move("next_phase")
        self.set_info("Next Turn")
        self.__hand_notebook.hide(self.__hands[self.__current_player])
        self.__current_player = (self.__current_player+1) % len(self.__hands)
        self.__hand_notebook.add(self.__hands[self.__current_player])
        self.__hand_notebook.select(self.__hands[self.__current_player])

    def zoom(self, img: Image):
        self.__info.zoom(img)

    def set_info(self, txt: str):
        self.__info.set_info(txt)

    @property
    def padding(self):
        return self.__padding