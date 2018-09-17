#!/usr/bin/env python3


from tkinter import Tk, Frame, Button, Label, PhotoImage, Message
from functools import partial, reduce
import random

DB = "res/words/places"
IMDB = "res/images/{}{}"


class HiddenWord():
    def __init__(self):
        self.word = self.generate_word()

        temp_list = []
        for _ in self.word:
            temp_list.append("_")
        self.hidden_word = reduce((lambda x, y: "{} {}".format(x, y)), temp_list)

    def get_word(self):
        return self.word

    def generate_word(self):
        with open(DB, "r") as file:
            lines = file.readlines()
        randomIndex = random.randint(0, len(lines) - 1)
        return lines[randomIndex].replace("\n","")

    def get_hidden_word(self):
        return self.hidden_word

    def __translate_index(self, index):
        return index * 2

    def __detect_finish(self):
        for index in range(0,len(self.word)):
            if self.hidden_word[self.__translate_index(index)] == "_":
                return False
        return True

    def reveal(self, letter):
        temp_word = self.word
        hidden_word_list = list(self.hidden_word)
        while letter in temp_word:
            index = temp_word.index(letter)
            hidden_index = self.__translate_index(index)
            hidden_word_list[hidden_index] = temp_word[index]
            temp_word = temp_word.replace(letter,"_",1)
        self.hidden_word = "".join(hidden_word_list)
        return self.__detect_finish()

class Hangman():
    def __init__(self, root):
        '''
            0-8 - game states
            9 - win condition
            10 - lose condition
        '''
        self.image_list = [IMDB.format(i, ".gif") for i in range(1, 10)] + [IMDB.format("win", ".gif"),
                                                                            IMDB.format("lose", ".gif")]
        self.image_current_index = 0
        self.IMAGE_INDEX_LAST_ATTEMPT = 8
        self.IMAGE_INDEX_WIN = 9
        self.IMAGE_INDEX_LOSE = 10

        self.STATUS_BAR_START = "Start playing"
        self.STATUS_BAR_CORRECT = "This word has letter {}"
        self.STATUS_BAR_INCORRECT = "No letter {}"
        self.STATUS_BAR_WIN = "Congratulations"
        self.STATUS_BAR_LOSE = "Shame on you"

        self.root = root
        self.root.resizable(width=False, height=False)

        self.root.update_idletasks()
        self.width = 500
        self.height = 500
        self.x = (self.root.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.root.winfo_screenheight() // 2) - (self.height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))

        self.buttons_frame_lower = Frame(height=30, width=self.width)
        self.buttons_frame_lower.pack(side="bottom")
        self.buttons_frame_upper = Frame(height=30, width=self.width)
        self.buttons_frame_upper.pack(side="bottom")

        self.button_new_game = Button(self.root,text="Start new game",command=self.__start_new_game)
        self.button_quit = Button(self.root, text="Quit", command=self.__quit)

        self.buttons = []
        letter = 0
        self.ABC = "abcdefghijklmnopqrstuvwxyz"
        for i in range(0, 13):
            button = Button(self.buttons_frame_upper, text=self.ABC[letter],
                            command=partial(self.pressed_letter, self.ABC[letter]))
            self.buttons.append(button)
            letter += 1
            self.buttons[i].pack(side="left")
        for i in range(13, 26):
            button = Button(self.buttons_frame_lower, text=self.ABC[letter],
                            command=partial(self.pressed_letter, self.ABC[letter]))
            self.buttons.append(button)
            letter += 1
            self.buttons[i].pack(side="left")

        self.guess_word = HiddenWord()
        self.word = Label(self.root, text=self.guess_word.get_hidden_word())
        self.word.pack(side="bottom")
        self.status_bar = Label(self.root, anchor="center", text=self.STATUS_BAR_START)
        self.status_bar.pack(side="bottom")

        img = PhotoImage(file=self.image_list[0])
        self.image = Label(root, image=img)
        self.image.image = img
        self.image.place(relx=0.5, rely=0.4, anchor="center")

    def pressed_letter(self, letter):
        self.buttons[self.ABC.index(letter)].config(state="disabled")
        if letter in self.guess_word.get_word():
            finished = self.guess_word.reveal(letter)
            self.word.config(text=self.guess_word.get_hidden_word())
            if finished:
                temp_image = PhotoImage(file=self.image_list[self.IMAGE_INDEX_WIN])
                self.image.config(image=temp_image)
                self.image.image = temp_image
                self.status_bar.config(text=self.STATUS_BAR_WIN)
                for button in self.buttons:
                    button.config(state="disabled")
                self.button_new_game.pack(anchor="n",side="top")
                self.button_quit.pack(anchor="n",side="top")
            else:
                self.status_bar.config(text=self.STATUS_BAR_CORRECT.format(letter))
        else:
            self.image_current_index += 1
            if (self.image_current_index > self.IMAGE_INDEX_LAST_ATTEMPT):
                temp_image = PhotoImage(file=self.image_list[self.IMAGE_INDEX_LOSE])
                self.image.config(image=temp_image)
                self.image.image = temp_image
                self.status_bar.config(text=self.STATUS_BAR_LOSE)
                for button in self.buttons:
                    button.config(state="disabled")
                self.button_new_game.pack(anchor="n", side="top")
                self.button_quit.pack(anchor="n", side="top")
            else:
                temp_image = PhotoImage(file=self.image_list[self.image_current_index])
                self.image.config(image=temp_image)
                self.image.image = temp_image
                self.status_bar.config(text=self.STATUS_BAR_INCORRECT.format(letter))

    def __start_new_game(self):
        self.root.destroy()
        root = Tk()
        # False alarm on pycharm, the following line is required
        hangman = Hangman(root)
        root.mainloop()

    def __quit(self):
        self.root.destroy()

class MainMenu:
    def __init__(self,root):
        self.root = root

        self.root.resizable(width=False,height=False)
        self.root.update_idletasks()
        self.width = 200
        self.height = 100
        self.x = (self.root.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.root.winfo_screenheight() // 2) - (self.height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))

        self.new_game_button = Button(self.root, text="New game", command=self.__new_game)
        self.new_game_button.place(anchor="center",relx=0.5,rely=0.3)

        self.new_game_button = Button(self.root, text="Quit", command=self.__quit)
        self.new_game_button.place(anchor="center",relx=0.5,rely=0.7)

    def __new_game(self):
        self.root.destroy()
        root = Tk()
        # False alarm on pycharm, the following line is required
        hangman = Hangman(root)
        root.mainloop()

    def __quit(self):
        self.root.destroy()

root = Tk()
main_menu = MainMenu(root)
root.mainloop()