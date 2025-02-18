from controller import Controller
import tkinter as tk
from dog.dog_interface import DogPlayerInterface
from frames.startPage import StartPage
from frames.gamePage import GamePage
from frames.deckPage import DeckPage
from tkinter import messagebox


class PlayerInterface(DogPlayerInterface):

    def __init__(self):
        self.controller = Controller()
        self.main_window = tk.Tk()
        self.config_main_window()
        self.controller.fill_pages(self.main_window)
        self.controller.show_frame("StartPage",)
        self.main_window.mainloop()

    def config_main_window(self):
        self.main_window.title('Inscryption')
        self.main_window.geometry('1920x1080')
        self.main_window.fullscreen = True
        self.main_window.bind("<F11>", self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.main_window.fullscreen = not self.main_window.fullscreen
        if self.main_window.fullscreen:
            self.main_window.attributes("-fullscreen", True)
        else:
            self.main_window.attributes("-fullscreen", False)
        return "break"
