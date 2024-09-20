import tkinter as tk
from font import *
from startPage import StartPage

class GamePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Game Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10) #possivel substituir por grid

        #gameButton = tk.Button(self, text="Voltar ao Menu", 
        #                    command=lambda:controller.show_frame(StartPage))
        #gameButton.pack()