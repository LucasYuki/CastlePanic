from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw
import Interface
from Distribuido import CastlePanicDistribuido
from Jogo import FaseTipo

class LayoutGame(ttk.Frame):
    __slots__ = ("__board", "__info", "__hands", "__hand_notebook", "__buttons",
        "__cancel_btn", "__play_btn", "__passar_btn", "__padding", "__buttons_height")

    def __init__(self, interface, jogo: CastlePanicDistribuido, **kwargs):
        self.__jogo = jogo
        self.__interface = interface
        super().__init__(interface, **kwargs)
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        self.bind("<Configure>", self.__on_resize)
        
        self.__padding = 5
        self.__buttons_height = 25
        
        self.__board = Interface.BoardView(self, jogo.get_tabuleiro())
        self.__info = Interface.InfoViewer(self, background="bisque")

        self.__hand_notebook = ttk.Notebook(self) 
        self.__hands = {}
        for idx, jogador in self.__jogo.jogadores.items():
            hand = Interface.HandViewer(self, background="bisque",
                                        jogador=jogador)
            self.__hands[idx] = hand
            self.__hand_notebook.add(hand, text=jogador.nome + " (%s)" %jogador.ordem)
        
        # Inicialização dos Botões                
        self.__buttons = ttk.Frame(self)
        self.__buttons.rowconfigure(0, weight=1)
        self.__buttons_showing = {}
        
        self.__descartar_btn = ttk.Button(self.__buttons, text="Descartar", command=self.descartar)
        self.__descartar_btn.grid(column=0, row=0, sticky=(N, W, E, S))
        self.__buttons.columnconfigure(0, weight=1)
        self.__buttons_showing[self.__descartar_btn] = True
        
        self.__jogar_btn = ttk.Button(self.__buttons, text="Jogar", command=self.jogar)
        self.__jogar_btn.grid(column=2, row=0, sticky=(N, W, E, S))
        self.__buttons.columnconfigure(2, weight=1)
        self.__buttons_showing[self.__jogar_btn] = True
        
        self.__passar_btn = ttk.Button(self.__buttons, text="Passar", command=self.passar)
        self.__passar_btn.grid(column=3, row=0, sticky=(N, W, E, S))
        self.__buttons.columnconfigure(3, weight=1)
        self.__buttons_showing[self.__passar_btn] = True

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

    def descartar(self):
        self.set_info("Descartar")
        carta = self.__hands[self.__jogo.get_mesa().jogador_no_controle.idx].selected
        if carta is not None:
            self.__interface.descartar_comprar(carta)

    def jogar(self):
        self.set_info("Jogar")
        carta = self.__hands[self.__jogo.get_mesa().jogador_no_controle.idx].selected
        if carta is not None:
            self.__interface.jogar_carta(carta)

    def passar(self):
        self.set_info("Passar")
        self.__interface.passar_jogada()

    def hide_button(self, button):
        if self.__buttons_showing[button]:
            button._grid_info = button.grid_info()
            button.grid_remove()
            self.__buttons_showing[button] = False
        
    def show_button(self, button):
        if not self.__buttons_showing[button]:
            button.grid(button._grid_info)
            self.__buttons_showing[button] = True
        
    def zoom(self, img: Image):
        self.__info.zoom(img)

    def set_info(self, txt: str):
        self.__info.set_info(txt)

    @property
    def padding(self):
        return self.__padding
    
    def update(self):
        fase = self.__jogo.get_fase()
        if fase == FaseTipo.INICIO:
            self.show_button(self.__descartar_btn)
            self.show_button(self.__jogar_btn)
            self.show_button(self.__passar_btn)
        elif fase == FaseTipo.DESCARTE:
            self.hide_button(self.__descartar_btn)
            self.show_button(self.__jogar_btn)
            self.show_button(self.__passar_btn)
        elif fase == FaseTipo.JOGADA:
            self.hide_button(self.__descartar_btn)
            self.hide_button(self.__jogar_btn)
            self.show_button(self.__passar_btn)
        elif fase == FaseTipo.VITORIA:
            self.hide_button(self.__descartar_btn)
            self.hide_button(self.__jogar_btn)
            self.hide_button(self.__passar_btn)
            self.set_info("VITORIA")
        elif fase == FaseTipo.DERROTA:
            self.hide_button(self.__descartar_btn)
            self.hide_button(self.__jogar_btn)
            self.hide_button(self.__passar_btn)
            self.set_info("DERROTA")
        
        self.__hand_notebook.select(self.__hands[self.__jogo.get_mesa().jogador_no_controle.idx])
        self.__board.update()
        for hand in self.__hands.values():
            hand.update()