from tkinter import Frame
from tkinter import Entry
from tkinter import Label
from tkinter import Canvas
from tkinter import Button
from tkinter import messagebox
from database.db_handler import *
from main import show_frame

import cv2
from PIL import Image, ImageTk

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
            # go_to_main_page(self)
        else:
            messagebox.showinfo('', 'Введите верные данные')


class MainWindow:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1280x720')
        self.window.minsize(1280, 720)
        self.window.title('Система распознавания лиц')
        self.window.resizable(0, 0)

        # Frames
        # =============================================================================================================
        # Background frames
        self.loginBackgroundFrame = Frame(
            self.window
        )
        self.loginBackgroundFrame.config(background='#afebee')
        self.loginBackgroundFrame.rowconfigure(0, weight=1)
        self.loginBackgroundFrame.columnconfigure(0, weight=1)

        self.mainFrameBackground = Frame(
            self.window,
        )
        self.mainFrameBackground.rowconfigure(0, weight=1)
        self.mainFrameBackground.columnconfigure(2, weight=1)
        self.mainFrameBackground.columnconfigure(1, weight=1)
        self.mainFrameBackground.columnconfigure(0, weight=1)

        # =============================================================================================================
        # Login frame
        self.loginCardFrame = Frame(
            self.loginBackgroundFrame,
            bg='#8e8d8a'
        )
        self.loginCardFrame.grid(sticky='wesn', row=0, column=0, pady=70, padx=450)
        self.loginCardFrame.rowconfigure(0, weight=1)
        self.loginCardFrame.columnconfigure(0, weight=1)

        # Labels
        self.userNameLabel = Label(
            self.loginCardFrame,
            text='Логин:',
            font=my_font,
            bg='#8e8d8a'
        )
        self.userNameLabel.grid(row=0, column=0, pady=20, padx=20)

        self.userPasswordLabel = Label(
            self.loginCardFrame,
            text='Пароль:',
            font=my_font,
            bg='#8e8d8a'
        )
        self.userPasswordLabel.grid(row=2, column=0, pady=20, padx=20)

        # Entry
        self.userNameEntry = Entry(
            self.loginCardFrame,
            font=my_font,
            highlightthickness=0,
            bg='#afebee',
            border=0
        )
        self.userNameEntry.grid(sticky='we', row=1, column=0, pady=20, padx=20)

        self.userPasswordEntry = Entry(
            self.loginCardFrame,
            font=my_font,
            highlightthickness=0,
            bg='#afebee',
            show='*',
            border=0
        )
        self.userPasswordEntry.grid(sticky='we', row=3, column=0, pady=20, padx=20)

        # Buttons
        self.auth_btn = Button(
            self.loginCardFrame,
            text='Авторизоваться',
            command=lambda: self.check_user()
        )
        self.auth_btn.grid(row=4, column=0, pady=20, sticky='we', padx=20)

        # =============================================================================================================
        # Main frame
        self.webcamFrame = Frame(
            self.mainFrameBackground,
            bg='#8e8d8a'
        )
        self.webcamFrame.grid(sticky='wens', row=0, column=0, pady=70, padx=20, columnspan=2)

        self.InfoCardFrame = Frame(
            self.mainFrameBackground,
            bg='red'
        )
        self.InfoCardFrame.grid(sticky='wens', row=0, column=2, pady=70, padx=20)

        self.f1 = Label(
            self.webcamFrame
        )
        self.f1.pack()

        self.L1 = Label(
            self.f1,
            bg='red'
        )
        self.L1.pack()

        self.webcam_btn = Button(
            self.InfoCardFrame,
            text='Авторизоваться',
            command=lambda: self.show_webcam()
        )
        self.webcam_btn.grid(row=0, column=0)

        # Logic
        for frame in (self.loginBackgroundFrame, self.mainFrameBackground):
            frame.grid(row=0, column=0, stick='wens')

        show_frame(self.loginBackgroundFrame)

    # commands
    def check_user(self):
        user_name = self.userNameEntry.get()
        user_password = self.userPasswordEntry.get()

        if user_name == '' or user_password == '':
            messagebox.showinfo('', 'Поля не должны быть пустыми')
        elif auth(user_name, user_password):
            self.window.state('zoomed')
            self.window.resizable(True, True)
            show_frame(self.mainFrameBackground)
        else:
            messagebox.showinfo('', 'Введите верные данные')

    def show_webcam(self):
        cap = cv2.VideoCapture(0)
        while True:
            img = cap.read()[1]
            # img = cv2.cvtColor((img, cv2.COLOR_BGR2RGB))
            img = ImageTk.PhotoImage(Image.fromarray(img))
            self.L1['image'] = img
            self.webcamFrame.update()
