import tkinter as tk
from fonts.font import *
from button import Button
from config import *
from PIL import Image, ImageTk

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        
        #self.set_background("images/backgroundMenu.jpg")

        label = tk.Label(self, text="Inscryption", font=LARGE_FONT)
        label.place(relx=0.5, rely=0.4, anchor="center")
        
        gameButton = Button(self, "Iniciar Partida", "show_frame", controller, ("GamePage", ))

        gameButton.place(relx=0.5, rely=0.6, anchor="center")

        deckButton = Button(self, "Criar Deck", "show_frame", controller, ("DeckPage", ))

        deckButton.place(relx=0.5, rely=0.7, anchor="center")

        exitButton = Button(self, "Sair do Jogo", "exit_game", controller)

        exitButton.place(relx=0.5, rely=0.8, anchor="center")

    def set_background(self, image_path):
        image = Image.open(image_path)
        image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)

        background_label = tk.Label(self, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)
