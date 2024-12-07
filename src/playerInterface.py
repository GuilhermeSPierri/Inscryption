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

    # Métodos adicionados
    def receive_withdraw(self): 
        pass

    def update_gui(self, game_state: dict): 
        pass

    def start_match(self): 
        pass

    def receive_move(self, a_move: dict): 
        pass

    def receive_det_start(self, start_status): 
        pass

    def invoke_card(self, carta): 
        pass

    def show_frame(self, page_name: str): 
        pass

    def add_card_to_interface(self, id: int): 
        pass

    def remove_card_from_interface(self, id: int): 
        pass

    def verify_deck(self): 
        pass

    def update_list_of_cards(self, list_of_cards): 
        pass

    def pass_turn(self): 
        pass

    def get_page(self, page_name: str): 
        pass

    def fill_pages(self): 
        pass

    def get_list_of_cards(self): 
        pass

    def buy_card(self, type: str): 
        pass

    def update_hand(self, hand): 
        pass

    def exit_game(self): 
        pass

    def select_card(self): 
        pass

    def select_position(self): 
        pass

    def reset_game(self): 
        pass

    def save_deck(self): 
        pass
