#!/usr/bin/env python3


from tkinter import Tk, Frame, Button, Label
from functools import partial

class Hangman():
    def __init__(self, root):
        self.width = 500
        self.height = 500
        self.root = root
        self.root.geometry("{}x{}".format(self.width,self.height));
        self.root.resizable(width=False, height=False)

        self.buttons_frame_lower = Frame(height=30, width=500)
        self.buttons_frame_lower.pack(side="bottom")
        self.buttons_frame_upper = Frame(height=30, width=500)
        self.buttons_frame_upper.pack(side="bottom")

        self.buttons = []
        letter = 0
        abc = "abcdefghijklmnopqrstuvwxyz"
        for i in range(0,13):
            button = Button(self.buttons_frame_upper, text=abc[letter], command=partial(self.pressed_letter,abc[letter]))
            self.buttons.append(button)
            letter += 1
            self.buttons[i].pack(side="left")
        for i in range(13,26):
            button = Button(self.buttons_frame_lower, text=abc[letter], command=partial(self.pressed_letter,abc[letter]))
            self.buttons.append(button)
            letter += 1
            self.buttons[i].pack(side="left")

    def pressed_letter(self,letter):
        print(letter)


root = Tk()
hangman = Hangman(root)
root.mainloop()
