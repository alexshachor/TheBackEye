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
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='black')
        self.v_img = PhotoImage(file='.\PicUi\\v.png')
        self.x_img = PhotoImage(file='.\PicUi\\x.png')
        self.img = PhotoImage(file='.\PicUi\\healthPic1.png')
        self.vv_img = PhotoImage(file='.\PicUi\\vv.png')
        self.xx_img = PhotoImage(file='.\PicUi\\xx.png')
        self.invalid = None
        self.pb = None
        self.health_controller = hc.HealthCheckPageController()
        self.background()
        self.input_output(controller)
        self.buttons(controller)

    def background(self):
        panel = tk.Label(self, image=self.img)
        panel.pack(expand=tk.YES, fill=tk.BOTH)
        pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
                                , bg='black', bd=0, fg='blue', font=FONT_OUTPUT)
        pure_sarcasm.place(bordermode=OUTSIDE, x=110, y=75)

    def input_output(self, controller):
        x = threading.Thread(target=lambda: self.show_components(controller))
        x.setDaemon(True)
        x.start()
        self.pb = sg.ShowGif(self)
        self.pb.config(bg='black')
        self.pb.show('.\\PicUi\\64x64.gif')
        self.pb.place(x=183, y=435)

    def show_components(self, controller):
        x = 50
        y = 150
        i = 0
        colors = ['blue', 'green', 'red', 'orange', 'black', 'grey']
        map = self.health_controller.get_health_map()
        for key, val in map.items():
            time.sleep(1)
            label = tk.Label(self, text=key, fg=colors[i], font=FONT_HEALTH, bg='white')
            label.place(bordermode=OUTSIDE, x=x, y=y)
            time.sleep(1)
            label = tk.Label(self, image=self.v_img, borderwidth=0) if val else \
                tk.Label(self, image=self.x_img, borderwidth=0)
            label.place(bordermode=OUTSIDE, x=x + 280, y=y + 5)
            y += 50
            i += 1
        self.pb.destroy()
        if self.health_controller.is_ready():
            tk.Label(self, image=self.vv_img, borderwidth=0).place(x=180, y=435)
            time.sleep(1)
            controller.manage_frame(lip.LogInPage)
        else:
            # TODO: give the student an appropriate message & opportunity to send us
            #  a message, then close the ui (or close the program).
            tk.Label(self, image=self.xx_img, borderwidth=0).place(x=180, y=435)

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
