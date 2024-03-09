import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font
from pynput import keyboard
import time
import random

def_frame = 0
green_frame = 0
yellow_frame = 0
grey_frame = 0
wordlefont = 0
root = 0
mainframe = 0


def frame_format():

    global def_frame
    global green_frame
    global yellow_frame
    global grey_frame
    global wordlefont

    def_frame = ttk.Style()
    def_frame.configure('black.TFrame',
                        background='black',
                        borderwidth=2,
                        relief='raised',
                        bordercolor='grey')

    green_frame = ttk.Style()
    green_frame.configure('green.TFrame',
                          background='green',
                          borderwidth=0,
                          relief='raised')

    yellow_frame = ttk.Style()
    yellow_frame.configure('yellow.TFrame',
                           background='yellow',
                           borderwidth=0,
                           relief='raised')

    grey_frame = ttk.Style()
    grey_frame.configure('darkgray.TFrame',
                         background='darkgrey',
                         borderwidth=0,
                         relief='raised')

    wordlefont = font.Font(family='Helvetica',
                           name='appHighlightFont',
                           size=30,
                           weight='bold')


def create_window():
    global root
    global mainframe

    root = Tk()
    root.title("Jondle3")
    frame_format()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    mainframe = tk.Frame(root, bg='black')
    mainframe.grid(column=0, row=0)

    for j in range(6):
        for i in range(5):
            box1 = ttk.Frame(mainframe,
                             width=75,
                             height=75,
                             style='black.TFrame')
            box1.grid(column=i, row=j, padx=3, pady=3)

    root.mainloop()


def on_press(key):
    if key == "endgame":
        return False

    try:
        k = key.char  # single-char keys
        k = k.upper()
    except:
        k = key.name  # other keys
    #print('Key pressed: ' + k) for debug
    if k in "QWERTYUIOPASDFGHJKLZXCVBNM" or k in ["backspace", "enter"]:
        handleKey(k)


def setWin(state):
    
    global root  
    time.sleep(1.5)

    end = tk.Toplevel(root)  
    end.title("Good Game")
    
    end.geometry('300x200')  

    screen = tk.Frame(end, bg='black')
    screen.pack(expand=True, fill="both")  

    if state:
        top = "Congrats!"
        bottom = "You Win"
        color = "green"
    else:
        top = "Sorry!"
        bottom = "You Lose"
        color = "red"
    
    # For displaying the secret word when the user loses
    if not state:
        letter = ttk.Label(screen, text=secret_word.upper(), font=wordlefont)
        letter.config(foreground=color, background='black')
        letter.grid(column=0, row=2, padx=10, pady=10)

    letterTop = ttk.Label(screen, text=top, font=wordlefont)
    letterTop.config(foreground=color, background='black')
    letterTop.grid(column=0, row=0, padx=10, pady=10)

    letterBottom = ttk.Label(screen, text=bottom, font=wordlefont)
    letterBottom.config(foreground=color, background='black')
    letterBottom.grid(column=0, row=1, padx=10, pady=10)


def addLetter(x, y, let):
    letter = ttk.Label(mainframe, text=let, font=wordlefont)
    letter.config(foreground='white', background='black')
    letter.grid(column=x, row=y)


def color(x, y, color, let):
    # Any 'let' longer than one character gives a blank frame
    if len(let) > 1:
        let = "   "
    
    # Using tk.Frame to directly apply background color
    box = tk.Frame(mainframe, width=75, height=75, bg=color)
    box.grid(column=x, row=y, padx=3, pady=3)
    
    # Placing the letter label inside the frame
    letter = tk.Label(box, text=let, font=wordlefont, bg=color, fg='white')
    letter.place(relx=0.5, rely=0.5, anchor="center")  # Center the label within the frame



#############################################################
#             IMPLEMENT CODE BELOW THIS LINE #############################################################
english_words = []
secret_word = ""
current_word = []
word_num = 0


def colorLogic():
    global word_num
    global current_word
    green_count = 0

    secret = []
    for i in secret_word:
        secret += [i.upper()]

    letter = 0
    for i in current_word:
        if i in secret:
            inde = secret.index(i)
            if inde == letter:
                color(letter, word_num, "green", i)
                green_count += 1
                current_word[inde] = "." #allow for dup letters
            else:
                color(letter, word_num, "yellow", i)
            secret[inde] = "-"
        else:
            color(letter, word_num, "darkgray", i)
        letter += 1

    word_num += 1
    current_word = []
    if green_count == 5:
        setWin(True)
    if word_num > 5:
        setWin(False)


def handleKey(key):
    global current_word

    if key == "enter":
        #print(secret_word,len(current_word)) for debugging
        if len(current_word) == 5:
            if validateWord():
                colorLogic()

    elif key == "backspace":
        if len(current_word) > 0:
            handleDelete()

    elif len(current_word) < 5:
        addLetter(len(current_word), word_num, key)
        current_word += [key]


def handleDelete():
    global current_word
    if len(current_word) > 0:
        current_word.pop()
        color(len(current_word), word_num, "lightgrey", "")


def getWord():
    global english_words
    global secret_word
    file = open("englishWords.txt", "r")

    for i in file:
        english_words += [i.strip()]

    file.close()
    secret_word = english_words[random.randint(0, len(english_words))]


def validateWord():
    word = ""
    for i in current_word:
        word += i

    for i in english_words:
        if i == word.lower():
            return True
    return False


def play():
    getWord()
    create_window()


play()
