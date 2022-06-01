import tkinter as tk
from gui import *


def show_frame(frame):
    frame.tkraise()


def app():
    window = tk.Tk()
    MainWindow(window)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    window.mainloop()


if __name__ == '__main__':
    app()
