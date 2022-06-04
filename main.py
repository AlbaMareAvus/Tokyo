from gui import *
import customtkinter as ctk


def show_frame(frame):
    frame.tkraise()


def app():
    window = ctk.CTk()
    MainWindow(window)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    window.mainloop()


if __name__ == '__main__':
    app()
