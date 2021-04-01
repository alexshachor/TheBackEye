from tkinter import *
import tkinter as tk
from Ui import progressbar
from UiController import logInPageController as lc
from Ui import overViewButtons as ovb
from Ui import takePicPage as tp
from Ui import uploadPicPage as up
import config as c
import threading

FONT_OUTPUT = c.APP['FONT_OUTPUT']


class LogInPage(tk.Frame):
    """
    This class is responsible for displaying the start page.
    """
    def __init__(self, parent, controller):
        """
        Init variables and calling functions.
        :param parent: the parent frame
        :param controller: gives the ability to switch between pages
        """
        tk.Frame.__init__(self, parent)
        self.login_img = PhotoImage(file='.\PicUi\\login_b.png')
        self.img = PhotoImage(file='.\PicUi\\login_background.png')
        self.invalid_name = None
        self.invalid_id = None
        self.pb = None
        # In these functions I will create & place all of the components
        # in the appropriate places, and run logic according to the user's requirements.
        self.background()
        self.name, self.id = self.input_output()
        self.buttons(controller)

    def background(self):
        """
        Init background.
        """
        panel = tk.Label(self, image=self.img)
        panel.place(bordermode=OUTSIDE)
        pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
                                , bg='black', bd=0, fg='blue', font=FONT_OUTPUT)
        pure_sarcasm.place(bordermode=OUTSIDE, x=135, y=85)

    def input_output(self):
        """
        Init input output.
        """
        name = tk.Label(self, text='Full Name:', bg='black', bd=0, fg='yellow', font=FONT_OUTPUT)
        name.place(bordermode=OUTSIDE, x=110, y=210)
        e_name = Entry(self)
        e_name.place(bordermode=OUTSIDE, x=110, y=235, width=220, height=40)
        id = tk.Label(self, text='Your ID:', bg='black', bd=0, fg='yellow', font=FONT_OUTPUT)
        id.place(bordermode=OUTSIDE, x=110, y=295)
        e_id = Entry(self)
        e_id.place(bordermode=OUTSIDE, x=110, y=320, width=220, height=40)
        return e_name, e_id

    def buttons(self, controller):
        """
        Init buttons.
        :param controller: gives the ability to switch between pages
        """
        login = tk.Button(self, image=self.login_img, borderwidth=0, background='black',
                          command=lambda: self.login_button(controller))
        login.place(bordermode=OUTSIDE, x=118, y=470)

    def login_button(self, controller):
        """
        The logic that occurs when the user clicks login.
        :param controller: gives the ability to switch between pages
        """
        obg = lc.LoginController(self.name.get(), self.id.get())
        msg = obg.check_validation('Name', self.name.get())
        if msg != 'OK':
            self.invalid_name = ovb.create_msg(self, 260, 275, msg)
        msg1 = obg.check_validation('ID', self.id.get())
        if msg1 != 'OK':
            self.invalid_id = ovb.create_msg(self, 260, 360, msg1)
        if msg == 'OK' and msg1 == 'OK':
            self.pb = progressbar.progressbar(self)
            self.pb.place(bordermode=OUTSIDE, x=118, y=420, height=30, width=200)
            self.pb.start()
            x = threading.Thread(target=lambda: self.check_for_pic(controller, obg))
            x.setDaemon(True)
            x.start()

    def check_for_pic(self, controller, obg):
        """
        Check if the user is on the system and has an updated image on the server.
        :param controller: gives the ability to switch between pages
        :param obg: the login controller
        """
        has_pic = obg.has_pic()
        self.pb.destroy()
        self.clean_entries()
        controller.manage_frame(tp.TakePicPage) if has_pic else controller.manage_frame(up.UploadPicPage)

    def clean_entries(self):
        """
        Clearing the page.
        """
        self.name.delete(0, 'end')
        self.id.delete(0, 'end')
        if self.invalid_id is not None:
            self.invalid_id.destroy()
        if self.invalid_name is not None:
            self.invalid_name.destroy()




