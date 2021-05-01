from tkinter import *
import tkinter as tk
import awesometkinter as atk
from Ui import progressbar
from UiController import validationController as vc
from Ui import overViewButtons as ovb
from Ui import uploadPicPage as up
import config as c
import threading

FONT_OUTPUT = c.APP['FONT_OUTPUT']


class ValidationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='black')
        self.email_img = PhotoImage(file='.\PicUi\\send.png')
        self.check_img = PhotoImage(file='.\PicUi\\check_pic.png')
        self.img = PhotoImage(file='.\PicUi\\validationPic.png')
        self.img1 = PhotoImage(file='.\PicUi\\validationPic1.png')
        self.email = ''
        self.count_flg = 0
        self.invalid_email = None
        self.invalid_code = None
        self.pb = None
        self.validation_controller = vc.ValidationController()
        self.bg = self.background()
        self.email_l, self.code_l, self.entry = self.input_output()
        self.email_b, self.check_b = self.buttons(controller)

    def background(self):
        panel = tk.Label(self, image=self.img)
        panel.pack(expand=tk.YES, fill=tk.BOTH)
        pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
                                , bg='black', bd=0, fg='blue', font=FONT_OUTPUT)
        pure_sarcasm.place(bordermode=OUTSIDE, x=110, y=75)
        return panel

    def input_output(self):
        pass

    def buttons(self, controller):
        pass

    def email_button(self, controller):
        pass

    def check_button(self, controller):
        pass

    def send_validation_code(self):
        pass

    def clean_entries(self):
        pass
