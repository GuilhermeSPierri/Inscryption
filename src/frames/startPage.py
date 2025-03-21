import tkinter as tk
from fonts.font import *
from widgets.button import Button
from config.config import *
from frames.page import Page
from tkinter import font
from PIL import Image, ImageTk
class StartPage(Page):

    def create_widgets(self):
        # Carregar a imagem de fundo
        self.bg_image = Image.open("images/backgroundMenu.jpg")  # Substitua pelo caminho real da imagem
        self.bg_image = self.bg_image.resize((1920, 1080))  # Ajuste o tamanho conforme necessário
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Criar um Label para exibir a imagem de fundo
        bg_label = tk.Label(self, image=self.bg_photo)
        bg_label.place(relwidth=1, relheight=1)  # Faz com que o fundo cubra toda a tela

        game_button = Button(self, "Iniciar  Partida", 18, 2, "start_match", self.controller,font=self.custom_font_buttons)
        game_button.place(relx=0.5, rely=0.67, anchor="center")

        deck_button = Button(self, "Criar  Deck", 18, 2, "show_frame", self.controller, ("DeckPage",), font=self.custom_font_buttons)
        deck_button.place(relx=0.5, rely=0.77, anchor="center")

        exit_button = Button(self, "Sair  do  Jogo", 18, 2, "leave_game", self.controller, font=self.custom_font_buttons)
        exit_button.place(relx=0.5, rely=0.87, anchor="center")

