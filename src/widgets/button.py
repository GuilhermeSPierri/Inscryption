import tkinter as tk


class Button(tk.Button):

    def __init__(self, parent, text, width, height, command, controller, args=()):
       
        super().__init__(parent, text=text, width=width, height=height, command=lambda: self.execute_command(command, controller, *args))

    def execute_command(self, command_name, controller, *args):
        
        command_function = getattr(controller, command_name, None)
        if command_function:
            command_function(*args)
        else:
            print(f"Command '{command_name}' not found in the controller.")