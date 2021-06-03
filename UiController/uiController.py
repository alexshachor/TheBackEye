import tkinter as tk
# from Ui import healthCheckPage as hcp
from Ui import uploadPicPage as hcp
from config import APP
import config as c


class TheBackEyeView(tk.Tk):
    """
    This is the class that is responsible for managing the page view,
    which means that the main part of the application is located here.
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)

        self.frames = {}
        # frame = hcp.HealthCheckPage(self.container, self)
        # self.frames[hcp.HealthCheckPage] = frame
        # frame.place(width=APP['WIDTH'], height=APP['HEIGHT'])
        # self.show_frame(hcp.HealthCheckPage)
        frame = hcp.UploadPicPage(self.container, self)
        self.frames[hcp.UploadPicPage] = frame
        frame.place(width=APP['WIDTH'], height=APP['HEIGHT'])
        self.show_frame(hcp.UploadPicPage)

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
