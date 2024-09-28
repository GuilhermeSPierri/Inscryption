import tkinter as tk
from fonts.font import *
from button import Button
from config import *
from PIL import Image, ImageTk

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.set_background("images/backgroundMenu.jpg")

        label = tk.Label(self, text="Inscryption", font=LARGE_FONT)
        label.pack(pady=10) #possivel substituir por grid
        
        
        gameButton = Button(self, "Jogar", "show_frame", controller, ("GamePage", ))

        gameButton.pack(pady=5)

        deckButton = Button(self, "Criar Deck", "show_frame", controller, ("DeckPage", ))

        deckButton.pack()

    def set_background(self, image_path):
        image = Image.open(image_path)
        image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)

        background_label = tk.Label(self, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)
