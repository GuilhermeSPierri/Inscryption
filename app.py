import tkinter as tk
from frames.startPage import StartPage  
from frames.gamePage import GamePage  
from frames.deckPage import DeckPage
from fonts.font import *

class ControllerApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        self.title('Inscryption')
        self.geometry('1920x1080')

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages = [StartPage, GamePage, DeckPage] # Add a new page here

        for page in pages:
            if page == StartPage:
                frame = page(container, self, lambda: self.show_frame(GamePage), lambda: self.show_frame(DeckPage)) 
            elif page == GamePage or page == DeckPage:
                frame = page(container, self, lambda: self.show_frame(StartPage))
            
            self.frames[page] = frame  
            frame.grid(row=0, column=0, sticky="nsew")



        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
