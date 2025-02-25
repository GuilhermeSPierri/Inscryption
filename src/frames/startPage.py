import tkinter as tk
from fonts.font import *
from widgets.button import Button
from config.config import *
from frames.page import Page

class StartPage(Page):

    def create_widgets(self):
        label = tk.Label(self, text="Inscryption", font=LARGE_FONT)
        label.place(relx=0.5, rely=0.4, anchor="center")

        game_button = Button(self, "Iniciar Partida", 20, 5, "start_match", self.controller)
        game_button.place(relx=0.5, rely=0.6, anchor="center")

        deck_button = Button(self, "Criar Deck", 20, 5, "show_frame", self.controller, ("DeckPage",))
        deck_button.place(relx=0.5, rely=0.7, anchor="center")

        exit_button = Button(self, "Sair do Jogo", 20, 5, "leave_game", self.controller)
        exit_button.place(relx=0.5, rely=0.8, anchor="center")

