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
import customtkinter as ctk
from face_detection import mtcnn_face_detection, haarcascade_face_detection

# font and font-size
my_font = ('yu gotic ui', 12)


# application theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(3, 1080)


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


class MainWindow(ctk.CTk):
    def __init__(self, window):
        self.window = window
        self.window.geometry('1280x720')
        self.window.minsize(1280, 720)
        self.window.title('Система распознавания лиц')
        self.window.resizable(0, 0)

        # Frames
        # =============================================================================================================
        # Background frames
        self.loginBackgroundFrame = ctk.CTkFrame(
            self.window,
            fg_color=('#ebebeb', '#1f1f1f'),
        )
        self.loginBackgroundFrame.rowconfigure(0, weight=1)
        self.loginBackgroundFrame.columnconfigure(0, weight=1)

        self.mainFrameBackground = ctk.CTkFrame(
            self.window,
            fg_color=('#ebebeb', '#1f1f1f'),
        )
        self.mainFrameBackground.columnconfigure(0, weight=9)
        self.mainFrameBackground.columnconfigure(1, weight=1)
        self.mainFrameBackground.rowconfigure(0, weight=8)
        self.mainFrameBackground.rowconfigure(1, weight=2)
        # =============================================================================================================
        # Login frame
        self.loginCardFrame = ctk.CTkFrame(
            self.loginBackgroundFrame,
            fg_color=('#d1d1d1', '#2e2e2e'),
        )
        self.loginCardFrame.grid(sticky='wesn', row=0, column=0, pady=30, padx=450)

        # Image
        self.user_login_image = Image.open('images/icons/user.png')
        login_image = ImageTk.PhotoImage(self.user_login_image)
        self.login_image_label = ctk.CTkLabel(self.loginCardFrame, image=login_image)
        self.login_image_label.image = login_image

        # Labels
        self.userNameLabel = ctk.CTkLabel(
            self.loginCardFrame,
            text='Логин:',
            text_font=my_font
        )

        self.userPasswordLabel = ctk.CTkLabel(
            self.loginCardFrame,
            text='Пароль:',
            text_font=my_font
        )

        # Entry
        self.userNameEntry = ctk.CTkEntry(
            self.loginCardFrame,
            text_font=my_font,
            placeholder_text='Введите логин...'
        )

        self.userPasswordEntry = ctk.CTkEntry(
            self.loginCardFrame,
            show='*',
            text_font=my_font,
            placeholder_text='Введите пароль...'
        )

        # Buttons
        self.auth_btn = ctk.CTkButton(
            self.loginCardFrame,
            text='Авторизоваться',
            text_font=my_font,
            command=lambda: self.check_user()
        )

        self.login_image_label.pack(pady=(80, 0))
        self.userNameLabel.pack(anchor='w', pady=(60, 0), padx=(0, 280))
        self.userNameEntry.pack(fill='x', padx=20, pady=(5, 0))
        self.userPasswordLabel.pack(anchor='w', pady=(20, 0), padx=(0, 268))
        self.userPasswordEntry.pack(fill='x', padx=20, pady=(5, 0))
        self.auth_btn.pack(fill='x', padx=20, pady=(30, 0))

        # =============================================================================================================
        # Main frame
        self.webcamFrame = ctk.CTkFrame(
            self.mainFrameBackground,
            fg_color=('#dedede', '#2e2e2e')
        )
        self.webcamFrame.columnconfigure(0, weight=1)
        self.webcamFrame.rowconfigure(0, weight=1)

        self.infoCardFrame = ctk.CTkFrame(
            self.mainFrameBackground,
            fg_color=('#dedede', '#2e2e2e')
        )
        
        self.settingsCardFrame = ctk.CTkFrame(
            self.mainFrameBackground,
            fg_color=('#dedede', '#2e2e2e')
        )

        self.f1 = ctk.CTkLabel(
            self.webcamFrame,
            text='',
            # fg_color=('#dedede', '#2e2e2e')
            fg_color='green'
        )
        self.f1.place(relwidth=1, relheight=1)

        self.webcam_btn = ctk.CTkButton(
            self.settingsCardFrame,
            text='Просто кнопка',
            text_font=my_font,
        )

        self.switch_theme = ctk.CTkSwitch(
            master=self.settingsCardFrame,
            text="Dark Mode",
            command=self.change_mode
        )

        self.webcamFrame.grid(sticky='wens', row=0, column=0, pady=40, padx=20, rowspan=2)
        self.infoCardFrame.grid(sticky='wens', row=0, column=1, pady=(40, 0), padx=20)
        self.settingsCardFrame.grid(sticky='wens', row=1, column=1, pady=(20, 40), padx=20)
        self.webcam_btn.pack(fill='x', padx=10, pady=(20, 0))
        self.switch_theme.pack(padx=10, pady=20, side='left')

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
            self.window.resizable(True, True)
            self.window.state('zoomed')
            show_frame(self.mainFrameBackground)
            self.show_webcam()
            self.switch_theme.select()
        else:
            messagebox.showinfo('', 'Введите верные данные')

    def show_webcam(self):
        print(int(cap.get(3)), int(cap.get(4)))
        while True:
            img = cap.read()[1]

            mtcnn_face_detection(img)
            # haarcascade_face_detection(img)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            self.f1['image'] = img
            self.webcamFrame.update()

        cap.release()
        cv2.destroyAllWindows()

    def change_mode(self):
        if self.switch_theme.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        self.window.state('zoomed')
