from customtkinter import CTk, CTkLabel, CTkButton
from PIL import ImageTk, Image
from numpy import *

class Window(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # variables creadas para centrar la ventana al iniciar el programa
        self.wtotal = self.winfo_screenwidth()
        self.htotal = self.winfo_screenheight()
        self.wventana = 900
        self.hventana = 740
        self.pwidth = round(self.wtotal/2-self.wventana/2)
        self.pheight = round(self.htotal/2-self.hventana/2)
        self.geometry(
            str(self.wventana)+"x"+str(self.hventana)+
            "+"+str(self.pwidth)+"+"+str(self.pheight-50))
        self.title('Mad Chess - Artificial Intelligence')
        self.resizable(0,0)
        
        self.images()

    def images(self):
        tablero_img = ImageTk.PhotoImage(
            Image.open('img/tablero.png'))
        # piezas blancas
        rey_blanco_img = ImageTk.PhotoImage(
            Image.open('img/rey-blanco.png'))
        dama_blanca_img = ImageTk.PhotoImage(
            Image.open('img/dama-blanca.png'))
        alfil_blanco_img = ImageTk.PhotoImage(
            Image.open('img/alfil-blanco.png'))
        caballo_blanco_img = ImageTk.PhotoImage(
            Image.open('img/caballo-blanco.png'))
        torre_blanca_img = ImageTk.PhotoImage(
            Image.open('img/torre-blanca.png'))
        peon_blanco_img = ImageTk.PhotoImage(
            Image.open('img/peon-blanco.png'))
        # piezas negras
        rey_negro_img = ImageTk.PhotoImage(
            Image.open('img/rey-negro.png'))
        dama_negra_img = ImageTk.PhotoImage(
            Image.open('img/dama-negra.png'))
        alfil_negro_img = ImageTk.PhotoImage(
            Image.open('img/alfil-negro.png'))
        caballo_negro_img = ImageTk.PhotoImage(
            Image.open('img/caballo-negro.png'))
        torre_negra_img = ImageTk.PhotoImage(
            Image.open('img/torre-negra.png'))
        peon_negro_img = ImageTk.PhotoImage(
            Image.open('img/peon-negro.png'))
        
        CTkLabel(master=self, text='', image=tablero_img).place(x=160,y=10)
        
        def tablero_inicial():
            posY = 51
            posX = 201
            # piezas negras arriba
            CTkLabel(master=self, text='', image=torre_negra_img).place(x=posX,y=posY)
        
        tablero_inicial()

if __name__=="__main__":
    window = Window()
    window.mainloop()
