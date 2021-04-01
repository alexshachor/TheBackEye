from tkinter import *
import tkinter as tk
from UiController import takePicPageController as tp
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
        self.background()

    def background(self):
        """
        Init background.
        """
        panel = tk.Label(self, image=self.img)
        panel.place(bordermode=OUTSIDE)
        # pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
        #                         , bg='black', bd=0, fg='green', font=FONT_OUTPUT)
        # pure_sarcasm.place(bordermode=OUTSIDE, x=135, y=85)
        x = threading.Thread(target=self.show_time)
        x.setDaemon(True)
        x.start()

    @staticmethod
    def show_time():
        """
        Show msg time.
        """
        time.sleep(SHOW_MSG_TIME)
        tp.successes()

