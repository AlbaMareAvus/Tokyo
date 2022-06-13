from tkinter import Frame
from tkinter import Entry
from tkinter import Label
from tkinter import Canvas
from tkinter import Button
from tkinter import messagebox
from tkinter import filedialog as fd
from database.db_handler import *
from main import show_frame
import cv2
from PIL import Image, ImageTk
import customtkinter as ctk
from face_detection import mtcnn_face_detection, haarcascade_face_detection
import shutil
import os
from face_recognition import update_dataset

# font and font-size
my_font = ('yu gotic ui', 12)
my_font_for_info_labels = ('yu gotic ui', 13)

photo_path = ''
knowing_faces_path = 'images/knowing_faces/'

# application theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)


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
        self.mainFrameBackground.columnconfigure(1, minsize=380)

        self.addPersonBackgroundFrame = ctk.CTkFrame(
            self.window,
            fg_color=('#ebebeb', '#1f1f1f'),
        )
        self.addPersonBackgroundFrame.rowconfigure(0, weight=1)
        self.addPersonBackgroundFrame.columnconfigure(0, weight=1)
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

        self.webcamLabel = ctk.CTkLabel(
            self.webcamFrame,
            text='',
            fg_color=('#dedede', '#2e2e2e')
            # fg_color='green'
        )
        self.webcamLabel.place(relwidth=1, relheight=1)

        self.add_person_btn = ctk.CTkButton(
            self.settingsCardFrame,
            text='Добавить людей',
            text_font=my_font,
            command=lambda: self.go_to_add_person_page()
        )

        self.refresh_database_btn = ctk.CTkButton(
            self.settingsCardFrame,
            text='Обновить базу',
            text_font=my_font,
            command=self.click_to_update_dataset
        )

        self.switch_theme = ctk.CTkSwitch(
            master=self.settingsCardFrame,
            text="Темная тема",
            command=self.change_mode,
            text_font=my_font
        )

        self.user_image = Image.open('images/icons/woman.png')
        img_size = (300, 300)
        self.user_image.thumbnail(img_size)
        person_image = ImageTk.PhotoImage(self.user_image)
        self.info_image_label = ctk.CTkLabel(self.infoCardFrame, image=person_image)
        self.info_image_label.image = person_image

        self.first_name_label_name = ctk.CTkLabel(
            self.infoCardFrame,
            text='Имя:',
            text_font=my_font_for_info_labels
        )

        self.second_name_label_name = ctk.CTkLabel(
            self.infoCardFrame,
            text='Фамилия:',
            text_font=my_font_for_info_labels
        )

        self.third_name_label_name = ctk.CTkLabel(
            self.infoCardFrame,
            text='Отчество:',
            text_font=my_font_for_info_labels
        )

        self.post_label_name = ctk.CTkLabel(
            self.infoCardFrame,
            text='Должность:',
            text_font=my_font_for_info_labels
        )

        self.webcamFrame.grid(sticky='wens', row=0, column=0, pady=40, padx=20, rowspan=2)
        self.infoCardFrame.grid(sticky='wens', row=0, column=1, pady=(40, 0), padx=20)
        self.settingsCardFrame.grid(sticky='wens', row=1, column=1, pady=(20, 40), padx=20)
        self.add_person_btn.pack(fill='x', padx=20, pady=(20, 0))
        self.refresh_database_btn.pack(fill='x', padx=20, pady=(20, 0))
        self.switch_theme.pack(padx=20, pady=20, side='left')
        self.info_image_label.pack(pady=(20, 0))
        self.second_name_label_name.pack(pady=(50, 0), fill='x')
        self.first_name_label_name.pack(pady=(20, 0), fill='x')
        self.third_name_label_name.pack(pady=(20, 0), fill='x')
        self.post_label_name.pack(pady=(20, 0), fill='x')

        # =============================================================================================================
        # Add Person frame
        self.addPersonCardFrame = ctk.CTkFrame(
            self.addPersonBackgroundFrame,
            fg_color=('#d1d1d1', '#2e2e2e'),
        )
        self.addPersonCardFrame.grid(sticky='wesn', row=0, column=0, pady=30, padx=450)

        self.first_name_label = ctk.CTkLabel(
            self.addPersonCardFrame,
            text='Имя:',
            text_font=my_font
        )

        self.second_name_label = ctk.CTkLabel(
            self.addPersonCardFrame,
            text='Фамилия:',
            text_font=my_font
        )

        self.third_name_label = ctk.CTkLabel(
            self.addPersonCardFrame,
            text='Отчество:',
            text_font=my_font
        )

        self.post_label = ctk.CTkLabel(
            self.addPersonCardFrame,
            text='Должность:',
            text_font=my_font
        )

        self.first_name_entry = ctk.CTkEntry(
            self.addPersonCardFrame,
            text_font=my_font,
            placeholder_text='Введите имя...'
        )

        self.second_name_entry = ctk.CTkEntry(
            self.addPersonCardFrame,
            text_font=my_font,
            placeholder_text='Введите фамилию...'
        )

        self.third_name_entry = ctk.CTkEntry(
            self.addPersonCardFrame,
            text_font=my_font,
            placeholder_text='Введите отчество...'
        )

        self.combobox = ctk.CTkOptionMenu(
            master=self.addPersonCardFrame,
            values=["Инженер-программист", "Тестировщик", "Начальник отдела"]
        )

        self.file_name_label = ctk.CTkLabel(
            self.addPersonCardFrame,
            text='Фото: ',
            text_font=my_font,
        )

        self.choose_file_btn = ctk.CTkButton(
            self.addPersonCardFrame,
            text='Добавить фото',
            text_font=my_font,
            command=self.choose_photo
        )

        self.add_person_btn = ctk.CTkButton(
            self.addPersonCardFrame,
            text='Добавить',
            text_font=my_font,
            command=self.add_person
        )

        self.second_name_label.pack(fill='x', pady=(60, 0))
        self.second_name_entry.pack(fill='x', padx=30, pady=(5, 0))
        self.first_name_label.pack(fill='x', pady=(60, 0))
        self.first_name_entry.pack(fill='x', padx=30, pady=(5, 0))
        self.third_name_label.pack(fill='x', pady=(60, 0))
        self.third_name_entry.pack(fill='x', padx=30, pady=(5, 0))
        self.post_label.pack(fill='x', pady=(60, 0))
        self.combobox.pack(fill='x', pady=(10, 0), padx=30)
        self.file_name_label.pack(fill='x', pady=(20, 0))
        self.choose_file_btn.pack(fill='x', pady=(10, 0), padx=30)
        self.add_person_btn.pack(fill='x', pady=(30, 0), padx=30)

        # Logic
        for frame in (self.loginBackgroundFrame, self.mainFrameBackground, self.addPersonBackgroundFrame):
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
            self.window.minsize(1536, 864)
            show_frame(self.mainFrameBackground)
            self.switch_theme.select()
            self.show_webcam()
        else:
            messagebox.showinfo('', 'Введите верные данные')

    def go_to_add_person_page(self):
        show_frame(self.addPersonBackgroundFrame)

    def show_webcam(self):
        while True:
            img = cap.read()[1]
            info = []

            img, is_verified_person = mtcnn_face_detection(img)
            # haarcascade_face_detection(img)

            if is_verified_person != '':
                staff_id = int(is_verified_person)
                first_name, second_name, third_name, post, img_path = get_info_about_person(staff_id)
                user_image = Image.open(img_path)
                img_size = (300, 300)
                user_image.thumbnail(img_size)
                person_image = ImageTk.PhotoImage(user_image)
                self.info_image_label.image = person_image
                self.info_image_label['image'] = self.info_image_label.image
                self.second_name_label_name.set_text('Фамилия: ' + second_name)
                self.first_name_label_name.set_text('Имя: ' + first_name)
                self.third_name_label_name.set_text('Отчество: ' + third_name)
                self.post_label_name.set_text('Должность: ' + post)
                self.info_image_label.configure(fg_color='green')
            else:
                person_image = ImageTk.PhotoImage(self.user_image)
                self.info_image_label.image = person_image
                self.info_image_label['image'] = self.info_image_label.image
                self.second_name_label_name.set_text('Фамилия: ')
                self.first_name_label_name.set_text('Имя: ')
                self.third_name_label_name.set_text('Отчество: ')
                self.post_label_name.set_text('Должность: ')
                self.info_image_label.configure(fg_color=('#dedede', '#2e2e2e'))

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            self.webcamLabel['image'] = img
            self.webcamFrame.update()

        cap.release()
        cv2.destroyAllWindows()

    def change_mode(self):
        if self.switch_theme.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        self.window.state('zoomed')

    def choose_photo(self):
        global photo_path
        photo_path = fd.askopenfilename(
            title='Выберите фото для загрузки в базу',
            filetypes=[
                ("image", ".jpeg"),
                ("image", ".png"),
                ("image", ".jpg"),
            ]
        )
        self.file_name_label.set_text(photo_path)

    def add_person(self):
        global photo_path, knowing_faces_path
        file_name = photo_path
        first_name = self.first_name_entry.get()
        second_name = self.second_name_entry.get()
        third_name = self.third_name_entry.get()
        post_name = self.combobox.get()
        print(first_name, second_name, third_name, post_name, file_name)
        if (
            first_name == '' or
            second_name == '' or
            third_name == '' or
            post_name == '' or
            file_name == ''
        ):
            messagebox.showinfo('', 'Поля не должны быть пустыми')
        else:
            shutil.copy(photo_path, knowing_faces_path)
            count_of_staff = str(get_count_of_staff() + 1)
            old_file_name, file_ext = os.path.splitext(photo_path)
            split_old_file_name = old_file_name.split('/')
            new_file_name = knowing_faces_path + count_of_staff + file_ext
            os.rename(knowing_faces_path + split_old_file_name[-1] + file_ext, new_file_name)
            add_person_to_database(first_name, second_name, third_name, post_name, new_file_name)
            self.clear_add_fields()
            show_frame(self.mainFrameBackground)

    def clear_add_fields(self):
        self.first_name_entry.delete("0", 'end')
        self.second_name_entry.delete("0", 'end')
        self.third_name_entry.delete("0", 'end')
        self.combobox.set("Инженер-программист")
        self.file_name_label.set_text("Фото: ")

    def click_to_update_dataset(self):
        update_dataset()
        messagebox.showinfo('', 'Перезапустите программу')
