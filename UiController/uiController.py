import tkinter as tk
from Ui import logInPage as lip
from config import APP
import config as c


# This is the class that is responsible for managing the page view,
# which means that the main part of the application is located here.
class TheBackEyeView(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)

        self.frames = {}
        frame = lip.LogInPage(self.container, self)
        self.frames[lip.LogInPage] = frame
        frame.place(width=APP['WIDTH'], height=APP['HEIGHT'])
        self.show_frame(lip.LogInPage)

    def show_frame(self, con):
        """
        Promote the requested page to the top of the queue.
        :param con: page
        """
        frame = self.frames[con]
        frame.tkraise()

    def add_frame(self, con):
        """
        Add new page to the queue.
        :param con: page
        """
        frame = con(self.container, self)
        self.frames[con] = frame
        frame.place(width=APP['WIDTH'], height=APP['HEIGHT'])

    def remove_frame(self, con):
        """
        Remove page from the queue.
        :param con: page
        """
        self.frames.pop(con)

    def manage_frame(self, con):
        """
        When moving between pages, keep the pages updated by rebuilding.
        :param con: page
        """
        if con in self.frames:
            self.remove_frame(con)
        self.add_frame(con)
        self.show_frame(con)


def run():
    """
    Create the main win for the app and keep it ruining.
    """
    c.APPLICATION = TheBackEyeView()
    c.APPLICATION.geometry(APP['WIN_SIZE'])
    c.APPLICATION.resizable(False, False)
    c.APPLICATION.title(APP['TITLE'])
    c.APPLICATION.iconbitmap('.\PicUi\\BackEye.ico')
    c.APPLICATION.mainloop()


def destructor():
    """
    Destroy the main win of the app.
    """
    c.APPLICATION.destroy()
