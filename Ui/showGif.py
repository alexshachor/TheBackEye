import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle


class ShowGif(tk.Label):

    def __init__(self, frame):
        super().__init__(frame)
        self.frames = None
        self.delay = None

    def load(self, root):
        pass

    def unload(self):
        pass

    def show_next_frame(self):
        pass


def for_tests_only():
    pass


if __name__ == "__main__":
    for_tests_only()
