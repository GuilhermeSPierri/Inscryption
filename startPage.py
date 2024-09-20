import tkinter as tk
from font import *
from gamePage import GamePage


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10) #possivel substituir por grid

        gameButton = tk.Button(self, text="Jogar", 
                            command=lambda:controller.show_frame(GamePage))
        gameButton.pack()

def qf(string):
    print(string)