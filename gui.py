import tkinter as tk
from tkinter import Frame

# font and font-size
my_font = ('consolas', 14)


class AuthWindow:
    def __init__(self, window):
        self.window = window
        self.window.title('Авторизация')
        self.window.geometry('1280x720')
        self.window.resizable(0, 0)
        self.window.state('zoomed')

        # Frames
