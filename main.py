import tkinter as tk

import gui
from gui import *

# if (window):
#     main_window = tk.Tk()
#     main_window.geometry('1920x1080')
#     main_window.title('asd')
#     main_window.resizable(0, 0)
#     main_window.state('zoomed')
#     main_window.mainloop()


def go_to_main_page(self):
    window = tk.Toplevel()
    gui.MainWindow(window)
    window.withdraw()
    window.deiconify()


def page():
    window = tk.Tk()
    AuthWindow(window)
    window.mainloop()


if __name__ == '__main__':
    page()

