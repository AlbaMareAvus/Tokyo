from tkinter import Frame
from tkinter import Entry
from tkinter import Label
from tkinter import Canvas
from tkinter import Button
from tkinter import messagebox
from database.db_handler import *
from main import go_to_main_page

# font and font-size
my_font = ('yu gotic ui', 13)


class AuthWindow:
    def __init__(self, window):
        self.window = window
        self.window.geometry('340x540'.format((window.winfo_screenwidth() // 2) - 640,
                                              (window.winfo_screenheight() // 2) - 360))
        self.window.title('Авторизация')
        self.window.resizable(0, 0)

        # Frames
        self.background = Frame(
            self.window,
            width=340,
            height=540,
            bg='#afebee'
        )
        self.background.place(x=0, y=0)

        # Labels
        self.userNameLabel = Label(
            self.background,
            text='Логин:',
            font=my_font,
            bg='#afebee'
        )
        self.userNameLabel.place(x=20, y=200)

        self.userPasswordLabel = Label(
            self.background,
            text='Пароль:',
            font=my_font,
            bg='#afebee'
        )
        self.userPasswordLabel.place(x=20, y=300)

        # Entry
        self.userNameEntry = Entry(
            self.background,
            font=my_font,
            highlightthickness=0,
            bg='#afebee',
            border=0
        )
        self.userNameEntry.place(x=20, y=240, width=300)

        self.userPasswordEntry = Entry(
            self.background,
            font=my_font,
            highlightthickness=0,
            bg='#afebee',
            show='*',
            border=0
        )
        self.userPasswordEntry.place(x=20, y=340, width=300)

        # Lines
        self.userNameLine = Canvas(
            self.background,
            width=300,
            height=1.5,
            bg='#fff',
            highlightthickness=0
        )
        self.userNameLine.place(x=20, y=268)

        self.userPasswordLine = Canvas(
            self.background,
            width=300,
            height=2.0,
            bg='#fff',
            highlightthickness=0
        )
        self.userPasswordLine.place(x=20, y=368)

        # Button
        self.authBtn = Button(
            self.background,
            text='Авторизоваться',
            cursor='hand2',
            font=my_font,
            command=self.check_user
        )
        self.authBtn.place(x=20, y=400)

    # commands
    def check_user(self):
        user_name = self.userNameEntry.get()
        user_password = self.userPasswordEntry.get()

        if user_name == '' or user_password == '':
            messagebox.showinfo('', 'Поля не должны быть пыстыми')
        elif auth(user_name, user_password):
            print(auth(user_name, user_password))
            go_to_main_page(self)
        else:
            messagebox.showinfo('', 'Введите верные данные')


class MainWindow:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1200x540')
        self.window.title('Система распознавания лиц')
        self.window.resizable(0, 0)

