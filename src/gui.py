from chessEngine import GameState
from customtkinter import CTk, CTkLabel, CTkButton
from tkinter import Canvas, PhotoImage

class Window(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gs = GameState()
        
        # variables creadas para centrar la ventana al iniciar el programa
        self.wtotal = self.winfo_screenwidth()
        self.htotal = self.winfo_screenheight()
        self.wventana = 720
        self.hventana = 760
        self.pwidth = round(self.wtotal/2-self.wventana/2)
        self.pheight = round(self.htotal/2-self.hventana/2)
        self.geometry(
            str(self.wventana)+"x"+str(self.hventana)+
            "+"+str(self.pwidth)+"+"+str(self.pheight-50))
        self.title('Mad Chess - Artificial Intelligence')
        self.resizable(0,0)
        
        self.posXTablero = 50
        self.posYTablero = 70
        self.imagenes = {}
        
        self.interfaz = Canvas(self)
        self.interfaz.place(
            x=self.posXTablero, y=self.posYTablero, width=640, height=640)
        self.dibujarTablero()
        self.cargarPiezas()
        self.mostrarPiezas()
        self.etiquetas()
        self.buttons()

    # Todo lo que hay que dibujar en pantalla
    def dibujarTablero(self):
        #self.interfaz.create_rectangle(x0,y0,x1,y1,fill='')
        tam_lado=80
        for i in range(8):
            for j in range(8):
                if (i+j)%2==0:
                    self.interfaz.create_rectangle(
                        i*tam_lado,j*tam_lado,
                        (i+1)*tam_lado,(j+1)*tam_lado,fill='#bac8d3')
                else:
                    self.interfaz.create_rectangle(
                        i*tam_lado,j*tam_lado,
                        (i+1)*tam_lado,(j+1)*tam_lado,fill='#18141d')

    def cargarPiezas(self):
        piezas = [
            'bR','bD','bA','bC','bT','bP',
            'nR','nD','nA','nC','nT','nP']
        for pieza in piezas:
            self.imagenes[pieza] = PhotoImage(file='./img/' + pieza + '.png')

    def mostrarPiezas(self):
        tam_lado=80
        for index_i, i in enumerate(self.gs.piezas):
            for index_j, j in enumerate(i):
                if j != '--':
                    self.interfaz.create_image(
                        index_j*tam_lado, index_i*tam_lado+1, image=self.imagenes[j], anchor='nw')
    # ------------------------

    def etiquetas(self):
        for i in range(8):
            CTkLabel(
                master=self, text=f'{8-i}', fg_color="transparent",
                width=40, height=30, font=('Comic Sans MS', 25)).place(x=5, y=80*i+95)
        letras=['A','B','C','D','E','F','G','H']
        for j in range(8):
            CTkLabel(
                master=self, text=f'{letras[j]}', fg_color="transparent",
                width=40, height=30, font=('Comic Sans MS', 25)).place(x=70+80*j, y=715)

    def buttons(self):
        # incialización e instanciados
        CTkButton(
            master=self, text="Start new game", #command=funcion_button_BFS,
            width=160, height=40, border_width=0, corner_radius=8, #state='disabled', text_color_disabled='white', 
            font=('Comic Sans MS', 20)).place(x=50, y=10)
        CTkButton(
            master=self, text="Return play", #command=funcion_button_BFS,
            width=160, height=40, border_width=0, corner_radius=8, #state='disabled', text_color_disabled='white', 
            font=('Comic Sans MS', 20)).place(x=290, y=10)
        # no se le ha dado funcion alguna
        CTkButton( # ni idea pa que lo creé
            master=self, text="Start new game", #command=funcion_button_BFS,
            width=160, height=40, border_width=0, corner_radius=8, #state='disabled', text_color_disabled='white', 
            font=('Comic Sans MS', 18))


if __name__=="__main__":
    window = Window()
    window.mainloop()
