import tkinter as tk
from frames.startPage import StartPage  
from frames.gamePage import GamePage  
from frames.deckPage import DeckPage
from fonts.font import *

class Controller(tk.Tk):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        self.title('Inscryption')
        self.geometry('1920x1080')
        self.fullscreen = True
        self.bind("<F11>", self.toggle_fullscreen)
        
        #self.bind("<Escape>", self.end_fullscreen)

        #self.overrideredirect(True)
    
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages = [StartPage, GamePage, DeckPage] # Add a new page here

        for page in pages:
            frame = page(container, self)
            self.frames[page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()

    def search_card(self, entry):
        print(entry.get())

    def on_check(self, var, card):
        state = var.get()
        print(f"{card} is {'selected' if state else 'deselected'}")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
           #self.overrideredirect(True)
            self.attributes("-fullscreen", True)
        else:
            #self.overrideredirect(False)
            self.attributes("-fullscreen", False)
        return "break"
    
    def end_fullscreen(self, event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)
        return "break"
    
    def exit_game(self):
        self.quit()

