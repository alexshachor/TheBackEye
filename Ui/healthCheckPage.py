from tkinter import *
import tkinter as tk
from Ui import showGif as sg
from UiController import healthCheckPageController as hc
from Ui import overViewButtons as ovb
from Ui import logInPage as lip
import config as c
import threading
import time

FONT_HEALTH = c.APP['FONT_HEALTH']
FONT_OUTPUT = c.APP['FONT_OUTPUT']


class HealthCheckPage(tk.Frame):

    def __init__(self, parent, controller):
        pass

    def background(self):
        pass

    def input_output(self, controller):
        pass

    def show_components(self, controller):
        pass

    def buttons(self, controller):
        pass
        # """
        # Init buttons.
        # :param controller: gives the ability to switch between pages
        # """
        # email_b = tk.Button(self, image=self.email_img, borderwidth=0, background='black',
        #                     command=lambda: self.email_button(controller))
        # email_b.place(bordermode=OUTSIDE, x=118, y=300)
        # check_b = tk.Button(self, image=self.check_img, borderwidth=0, background='black',
        #                     command=lambda: self.check_button(controller))
        # return email_b, check_b

    def clean_entries(self):
        pass
        # """
        # cleaning the page entries.
        # """
        # if self.invalid_email is not None:
        #     self.invalid_email.destroy()
        # if self.invalid_code is not None:
        #     self.invalid_code.destroy()