# fonts/font.py
import tkinter.font as tkfont
from tkinter import font
import ctypes
import os

# Tamanhos pré-definidos
SMALL_FONT = ("Helvetica", 10)
MEDIUM_FONT = ("Helvetica", 12)
LARGE_FONT = ("Helvetica", 14, "bold")

# Caminho da fonte
FONT_PATH = os.path.join("fonts", "fontInscryption.ttf")

# Registrar a fonte personalizada
ctypes.windll.gdi32.AddFontResourceW(FONT_PATH)