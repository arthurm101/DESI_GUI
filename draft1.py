from tkinter import *
from PIL import ImageTk
from PIL import Image

def clicked():
    lbl.configure(text="ya pressed it")

window = Tk()
window.title("hey oh")
window.geometry('785x400')

label = Label(window, text="Hello", font=("Calibri", 16))
label.grid(column=0, row=1)

# lbl2 = Label(window, text="Hello", font=("Calibri", 16))
# lbl2.grid(column=1, row=1)

# lbl2 = Label(window, text="Hello", font=("Calibri", 16))
# lbl2.grid(column=2, row=2)

backdropimg = Image.open("backdrop.jpg")
logo = Image.open("logo.jpg")
logo = logo.resize((150,120), Image.ANTIALIAS)
backdropimg.paste(logo, (20, 40))
backdropimg = ImageTk.PhotoImage(backdropimg)
backdrop = Label(window, image=backdropimg, text="DESI", fg="white", font=("Calibri",48), compound=CENTER)
backdrop.grid(column=0, row=0)
backdrop.image = backdropimg

# window.columnconfigure(0, weight=1)
# window.rowconfigure(0, weight=1)
# window.columnconfigure(1, weight=1)
# window.rowconfigure(1, weight=1)
# window.columnconfigure(2, weight=1)
# window.rowconfigure(2, weight=1)


button = Button(window, text="placeholder", bg="white", font=("Calibri",10), command=clicked)
button.grid(column=0, row=2)

textbox = Entry(window,width=10)
textbox.grid(column=0,row=3)

text.focus()
window.mainloop()

#780x207
#4868x3953





