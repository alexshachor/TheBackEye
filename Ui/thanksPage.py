from tkinter import *
import tkinter as tk
from UiController import takePicPageController as tp
from UiController import thanksPageController as tpc
import config as c
import time
import threading

FONT_OUTPUT = c.APP['FONT_OUTPUT']
FONT_MSG = c.APP['FONT_MSG']
SHOW_MSG_TIME = 20


class TanksPage(tk.Frame):
    """
    This class is responsible for displaying the Tanks Page.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.img = PhotoImage(file='.\PicUi\\tanks_background.png')
        self.hour = StringVar()
        self.minute = StringVar()
        self.second = StringVar()
        self.background()

    def background(self):
        """
        Init background.
        """
        panel = tk.Label(self, image=self.img)
        panel.pack(expand=tk.YES, fill=tk.BOTH)
        # pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
        #                         , bg='black', bd=0, fg='green', font=FONT_OUTPUT)
        # pure_sarcasm.place(bordermode=OUTSIDE, x=135, y=85)
        x = threading.Thread(target=self.show_time)
        x.setDaemon(True)
        x.start()

    def show_time(self):
        """
        Show msg time.
        """
        hour, minute = tpc.get_time_remaining()
        if hour == 'X':
            time.sleep(5)
            tp.successes()
            return
        self.hour.set(hour)
        self.minute.set(minute)
        self.second.set('00')
        label = tk.Label(self, text='The lesson will begin in:'
                         , bg='black', bd=0, fg='green', font=FONT_MSG)
        label.place(bordermode=OUTSIDE, x=60, y=420)
        hour_entry = Entry(self, width=3, font=("Arial", 18, ""), textvariable=self.hour)
        hour_entry.place(x=60, y=470)
        minute_entry = Entry(self, width=3, font=("Arial", 18, ""), textvariable=self.minute)
        minute_entry.place(x=110, y=470)
        second_entry = Entry(self, width=3, font=("Arial", 18, ""), textvariable=self.second)
        second_entry.place(x=160, y=470)
        self.submit()
        tp.successes()

