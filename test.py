from tkinter import *
from threading import Thread

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

def send():
    print

def new(root):
    new = Toplevel(root)
    new.title("Menu")
    outputText = Text(new, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    outputText.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(outputText)
    scrollbar.place(relheight=1, relx=0.974)
    inputText = Entry(new, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    inputText.grid(row=2, column=0)
    Button(new, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)

root = Tk()
root.title("Menu")
outputText = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
outputText.grid(row=1, column=0, columnspan=2)
scrollbar = Scrollbar(outputText)
scrollbar.place(relheight=1, relx=0.974)
inputText = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
inputText.grid(row=2, column=0)
Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)

t = Thread(target=new, args=(root,), daemon=True)
t.start()

root.mainloop()
