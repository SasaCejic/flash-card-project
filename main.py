from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
INFO_FONT = ("Arial", 40)

words_dict = []
word_pair = {}
words_to_learn = []

# Reading the words
def read_words():
    global words_dict
    try:
        df = pandas.read_csv("data/words_to_learn.csv")
    except (FileNotFoundError, pandas.errors.EmptyDataError):
        df = pandas.read_csv("data/french_words.csv")
    finally:
        words_dict = df.to_dict(orient="records")

def pick_a_random_pair():
    global words_dict
    global word_pair

    if len(words_dict) > 0:
        word_pair = random.choice(words_dict)
    else:
        global canvas
        global wrong_button
        global right_button
        canvas.delete("title")
        canvas.delete("word")
        canvas.delete("image")
        wrong_button.destroy()
        right_button.destroy()
        canvas.destroy()

        new_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
        new_canvas.create_text(400, 263, text="No more words to display!", font=INFO_FONT, fill="white")
        new_canvas.grid(row=0, column=0, columnspan=2)

def show_card_front():
    global canvas

    if canvas.winfo_exists():
        global word_pair
        global card_front
        global words_dict

        canvas.create_image(400, 263, image=card_front, tags="image")
        canvas.delete("title")
        canvas.delete("word")
        canvas.create_text(400, 150, text="French", font=TITLE_FONT, tags="title")
        canvas.create_text(400, 263, text=word_pair["French"], font=WORD_FONT, tags="word")


def show_card_back():
    global canvas

    if canvas.winfo_exists():
        global word_pair
        global card_back
        canvas.create_image(400, 263, image=card_back, tags="image")
        canvas.delete("title")
        canvas.delete("word")
        canvas.create_text(400, 150, text="English", font=TITLE_FONT, fill="white", tags="title")
        canvas.create_text(400, 263, text=word_pair["English"], font=WORD_FONT, fill="white", tags="word")

def wrong():
    global flip_timer, words_to_learn, word_pair
    window.after_cancel(flip_timer)
    words_to_learn.append(word_pair)
    pick_a_random_pair()
    show_card_front()
    flip_timer = window.after(3000, show_card_back)

def right():
    global flip_timer, words_dict, word_pair
    window.after_cancel(flip_timer)
    words_dict.remove(word_pair)
    pick_a_random_pair()
    show_card_front()
    flip_timer = window.after(3000, show_card_back)

def save_words_to_learn():
    global words_to_learn
    if len(words_to_learn) > 0:
        pandas.DataFrame(words_to_learn).to_csv("data/words_to_learn.csv", index=False)

read_words()

# UI Setup

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

pick_a_random_pair()
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas.create_image(400, 263, image=card_front, tags="image")
canvas.create_text(400, 150, text="French", font=TITLE_FONT, tags="title")
canvas.create_text(400, 263, text=word_pair["French"], font=WORD_FONT, tags="word")
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, borderwidth=0, highlightthickness=0, command=wrong)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, borderwidth=0, highlightthickness=0, command=right)
right_button.grid(row=1, column=1)

flip_timer = window.after(3000, show_card_back)

window.mainloop()

save_words_to_learn()