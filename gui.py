#!/usr/bin/python
from Tkinter import *
import os
import tempfile

class UI:
    root = None
    btnStart = None
    ICON_PATH = None

    def replaceLogo(self):
        ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
                b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
                b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64
        _, self.ICON_PATH = tempfile.mkstemp()
        with open(self.ICON_PATH, 'wb') as icon_file:
            icon_file.write(ICON)


    def initWidgets(self):
        self.replaceLogo()
        self.root = Tk()
        self.root.iconbitmap(default=self.ICON_PATH)
        self.root.wm_title("video duplicate removal")

    def Run(self):
        self.root.mainloop()


if __name__ == '__main__':
    ui = UI()
    ui.initWidgets()
    ui.Run()
