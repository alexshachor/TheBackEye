from tkinter import *
import tkinter as tk
from Ui import progressbar
from UiController import logInPageController as lc
from Ui import overViewButtons as ovb
from Ui import takePicPage as tp
from Ui import validationPage as vp
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
        self.name, self.id, self.class_code = self.input_output()
        self.buttons(controller)

    def background(self):
        """
        Init background.
        """
        panel = tk.Label(self, image=self.img)
        panel.pack(expand=tk.YES, fill=tk.BOTH)
        pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
                                , bg='black', bd=0, fg='blue', font=FONT_OUTPUT)
        pure_sarcasm.place(bordermode=OUTSIDE, x=135, y=85)

    def input_output(self):
        """
        Init input output.
        """
        name = tk.Label(self, text='Full Name:', bg='black', bd=0, fg='yellow', font=FONT_OUTPUT)
        name.place(bordermode=OUTSIDE, x=110, y=185)
        e_name = Entry(self)
        e_name.place(bordermode=OUTSIDE, x=110, y=205, width=220, height=40)
        id = tk.Label(self, text='Your ID:', bg='black', bd=0, fg='yellow', font=FONT_OUTPUT)
        id.place(bordermode=OUTSIDE, x=110, y=255)
        e_id = Entry(self)
        e_id.place(bordermode=OUTSIDE, x=110, y=275, width=220, height=40)
        class_code = tk.Label(self, text='Class Code:', bg='black', bd=0, fg='yellow', font=FONT_OUTPUT)
        class_code.place(bordermode=OUTSIDE, x=110, y=325)
        e_class_code = Entry(self)
        e_class_code.place(bordermode=OUTSIDE, x=110, y=345, width=220, height=40)
        return e_name, e_id, e_class_code

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
            self.invalid_name = ovb.create_msg(self, 260, 245, msg)
            return
        msg1 = obg.check_validation('ID', self.id.get())
        if msg1 != 'OK':
            self.invalid_id = ovb.create_msg(self, 260, 315, msg1)
            return
        msg2 = obg.check_class_code(self.class_code.get())
        if msg2 != 'OK':
            self.invalid_id = ovb.create_msg(self, 260, 385, msg1)
            return
        if msg == 'OK' and msg1 == 'OK' and msg2 == 'OK':
            c.USER_DATA['USERNAME'] = self.name.get()
            c.USER_DATA['ID'] = self.id.get()
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
        has_pic = obg.has_pic_and_email()
        self.pb.destroy()
        self.clean_entries()
        if has_pic == 'ToValidation':
            controller.manage_frame(vp.ValidationPage)
        elif has_pic == 'ToUpload':
            controller.manage_frame(up.UploadPicPage)
        elif has_pic == 'ToSnapshot':
            controller.manage_frame(tp.TakePicPage)

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




