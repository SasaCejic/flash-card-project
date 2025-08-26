from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")

word_pair = None

# Reading the words
def read_words():
    df = pandas.read_csv("data/french_words.csv")
    words_dict = df.to_dict(orient="records")
    return words_dict

def pick_a_random_pair():
    global word_pair
    words_dict = read_words()
    word_pair = random.choice(words_dict)

def show_card_front():
    global canvas
    global card_front
    pick_a_random_pair()
    canvas.create_image(400, 263, image=card_front, tags="image")
    canvas.delete("title")
    canvas.delete("word")
    canvas.create_text(400, 150, text="French", font=TITLE_FONT, tags="title")
    canvas.create_text(400, 263, text=word_pair["French"], font=WORD_FONT, tags="word")

def show_card_back():
    global word_pair
    global canvas
    global card_back
    canvas.create_image(400, 263, image=card_back, tags="image")
    canvas.delete("title")
    canvas.delete("word")
    canvas.create_text(400, 150, text="French", font=TITLE_FONT, tags="title")
    canvas.create_text(400, 263, text=word_pair["English"], font=WORD_FONT, tags="word")
    canvas.config()

# UI Setup

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas.create_image(400, 263, image=card_front, tags="image")
canvas.create_text(400, 150, text="Title", font=TITLE_FONT, tags="title")
canvas.create_text(400, 263, text="Word", font=WORD_FONT, tags="word")
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, borderwidth=0, highlightthickness=0, command=show_card_front)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, borderwidth=0, highlightthickness=0, command=show_card_front)
right_button.grid(row=1, column=1)

window.mainloop()

