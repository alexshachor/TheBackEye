from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from Ui import progressbar
from UiController import uploadPicPageController as uc
from Ui import takePicPage as tp
from Ui import overViewButtons as ovb
import config as c
import threading

FONT_OUTPUT = c.APP['FONT_OUTPUT']
FONT_MSG = c.APP['FONT_MSG']


class UploadPicPage(tk.Frame):
    """
    This class is responsible for displaying the Upload Pic Page.
    """
    def __init__(self, parent, controller):
        """
        Init variables and calling functions.
        :param parent: the parent frame
        :param controller: gives the ability to switch between pages
        """
        tk.Frame.__init__(self, parent)
        self.select_img = PhotoImage(file='.\PicUi\\select_image.png')
        self.upload_img = PhotoImage(file='.\PicUi\\upload_image.png')
        self.img = PhotoImage(file='.\PicUi\\as.png')
        self.invalid_pic = None
        self.pb = None
        self.user_image = None
        self.background()
        self.upload = self.buttons(controller)

    def background(self):
        """
        Init background.
        """
        panel = tk.Label(self, image=self.img)
        panel.place(bordermode=OUTSIDE)
        pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
                                , bg='black', bd=0, fg='yellow', font=FONT_OUTPUT)
        pure_sarcasm.place(bordermode=OUTSIDE, x=140, y=95)
        note = tk.Label(self, text='Note here!', bg='black', bd=0, fg='blue', font=FONT_MSG)
        note.place(bordermode=OUTSIDE, x=40, y=105)
        msg = 'Please upload a good photo of your pace\n''in png/jpg format.'
        ovb.create_tool_tip(note, text=msg)

    def buttons(self, controller):
        """
        Init buttons.
        :param controller: gives the ability to switch between pages
        :return upload: the upload button
        """
        select_img = Button(self, image=self.select_img, borderwidth=0, background='black',
                            command=self.open_img)
        select_img.place(bordermode=OUTSIDE, x=118, y=130)
        upload = tk.Button(self, image=self.upload_img, borderwidth=0, background='black',
                           command=lambda: self.upload_button(controller))
        return upload

    def open_img(self):
        """
        Open & show image from pc folders.
        """
        self.clean_entries()
        # Select the Imagename  from a folder
        x = self.open_file_name()
        # Opens the image
        try:
            img = Image.open(x)
        except:
            self.invalid_pic = ovb.create_msg(self, 118, 174,'Please try uploading only an image file.')
            return
        self.user_image = img
        # Resize the image and apply a high-quality down sampling filter
        img = img.resize((300, 300), Image.ANTIALIAS)
        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)
        panel = Label(self, image=img)
        # Set the image as img
        panel.image = img
        panel.place(bordermode=OUTSIDE, x=65, y=185)
        self.upload.place(bordermode=OUTSIDE, x=118, y=500)

    @staticmethod
    def open_file_name():
        """
        Open file dialog box to select image
        the dialogue box has a title "Open".
        """
        filename = filedialog.askopenfilename(title='"pen')
        return filename

    def upload_button(self, controller):
        """
        The logic that occurs when the user clicks upload.
        :param controller: gives the ability to switch between pages
        """
        self.pb = progressbar.progressbar(self)
        self.pb.place(bordermode=OUTSIDE, x=118, y=500, height=42, width=200)
        self.pb.start()
        x = threading.Thread(target=lambda: self.send_user_pic(controller))
        x.setDaemon(True)
        x.start()

    def send_user_pic(self, controller):
        """
        Check if the user image is a good image, if not show msg, if yes
        send him to the next page.
        :param controller: gives the ability to switch between pages
        """
        send_pic = uc.upload_pic(self.user_image)
        if send_pic == 'OK':
            self.pb.destroy()
            controller.manage_frame(tp.TakePicPage)
        else:
            self.invalid_pic = ovb.create_msg(self, 118, 490, send_pic)

    def clean_entries(self):
        """
        Clearing the page.
        """
        if self.invalid_pic is not None:
            self.invalid_pic.destroy()
