#python setup
from tkinter import *
from PIL import ImageTk
from PIL import Image
from tkinter import ttk
donebefore = 0
positionerIDcount = 0
y = 0

#functions to create widgets
def infotextboxSetup():
    if donebefore == 1:
        givensteplabel.grid_remove()
        givennamelabel.grid_remove()
        givendatelabel.grid_remove()

    global steptextbox,nametextbox,datetextbox
    steptextbox = Entry(infoFrame,width=10)
    steptextbox.grid(column=1,row=0)

    nametextbox = Entry(infoFrame,width=10)
    nametextbox.grid(column=1,row=1)

    datetextbox = Entry(infoFrame,width=10)
    datetextbox.grid(column=1,row=2)

    steptextbox.focus()

def positionerIDtextboxSetup():
    global positionerIDtextbox
    positionerIDtextbox = Entry(positionerIDtextboxframe,width=10)
    positionerIDtextbox.grid(column=1,row=0)

def infotextboxOverwriting(step,name,date):
    steptextbox.grid_remove()
    nametextbox.grid_remove()
    datetextbox.grid_remove()

    givensteplabel = Label(infoFrame, text=step, font=("Arial", 16))
    givensteplabel.grid(column=1, row=0)

    givennamelabel = Label(infoFrame, text=name, font=("Arial", 16))
    givennamelabel.grid(column=1, row=1)

    givendatelabel = Label(infoFrame, text=date, font=("Arial", 16))
    givendatelabel.grid(column=1, row=2)

    donebefore = 1

def positionerIDsgivenlabels(givenID,positionerIDcount):
    global y
    if positionerIDcount < 5:
        x = 0
    elif 5 <= positionerIDcount < 10:
        x = 1
    elif 10 <= positionerIDcount < 15:
        x = 2
    elif 15 <= positionerIDcount < 20:
        x = 3
    
    test = Label(IDlistframe, text=givenID, font=("Arial,12"))
    test.grid(column=x, row=y)

    if y == 4:
        y = 0
    else:
    	y = y + 1

#operation functions
def infobuttonclicked():
    step = steptextbox.get()
    name = nametextbox.get()
    date = datetextbox.get()
    infotextboxOverwriting(step, name, date)
    positionerIDtextbox.focus()
    IDlistframe.destroy()

def positionerIDbuttonclicked():
    global positionerIDcount,IDlistframe
    givenID = positionerIDtextbox.get()
    if positionerIDcount == 0:
    	IDlistframe = Frame(window)
    	IDlistframe.grid(column=2,row=2)
    if positionerIDcount == 19:
        positionerIDsgivenlabels(givenID,positionerIDcount)
        infotextboxSetup()
        steptextbox.focus()
        positionerIDcount = 0
    else:
        positionerIDsgivenlabels(givenID,positionerIDcount)
        positionerIDcount = positionerIDcount + 1

def go_to_next_entry(event, entry_list, this_index):
    next_index = (this_index + 1) % len(entry_list)
    entry_list[next_index].focus_set()




#gui setup
window = Tk()
window.title("hey oh")
window.geometry('785x500')
positionerIDtextboxframe = Frame(window)
IDlistframe = Frame(window)
infoFrame = Frame(window)

#image setup
backdropimg = Image.open("backdrop.jpg")
logo = Image.open("logo.jpg")
logo = logo.resize((150,120), Image.ANTIALIAS)
backdropimg.paste(logo, (20, 40))
backdropimg = ImageTk.PhotoImage(backdropimg)
backdrop = Label(window, image=backdropimg, text="DESI", fg="white", font=("Calibri",48), compound=CENTER)
backdrop.grid(column=0, row=0, columnspan=3)
backdrop.image = backdropimg



#info input
steplabel = Label(infoFrame, text="Step:", font=("Arial", 16))
steplabel.grid(column=0, row=0)

namelabel = Label(infoFrame, text="Name:", font=("Arial", 16))
namelabel.grid(column=0, row=1)

datelabel = Label(infoFrame, text="Date:", font=("Arial", 16))
datelabel.grid(column=0, row=2)

infobutton = Button(infoFrame, text="Enter", bg="white", font=("Calibri",10), command=infobuttonclicked)
infobutton.grid(column=1, row=3)

infoFrame.grid(column=0,row=3)



#Lines
verticalline = ttk.Separator(window,orient=VERTICAL)
verticalline.grid(column=1,row=1,rowspan=11,sticky="ns")
horizontalline = ttk.Separator(window,orient=HORIZONTAL)
horizontalline.grid(column=0,row=2,columnspan=11,sticky="ew")


#ID input
positionerIDlabel = Label(positionerIDtextboxframe, text="Positioner ID:", font=("Arial", 16))
positionerIDlabel.grid(column=0, row=0)

positionerIDbutton = Button(positionerIDtextboxframe, text="Enter", bg="white", font=("Calibri",10), command=positionerIDbuttonclicked)
positionerIDbutton.grid(column=1, row=1)

positionerIDtextboxframe.grid(column=2,row=3)
IDlistframe.grid(column=2,row=4)







#Entry connections
entries = [child for child in window.winfo_children() if isinstance(child, Entry)]
for idx, entry in enumerate(entries):
    entry.bind('<Return>', lambda e, idx=idx: go_to_next_entry(e, entries, idx))












#Operation
infotextboxSetup()
positionerIDtextboxSetup()
window.mainloop()








#Pic Sizes
#780x207
#4868x3953

#Column config
# window.columnconfigure(0, weight=1)
# window.rowconfigure(0, weight=1)
# window.columnconfigure(1, weight=1)
# window.rowconfigure(1, weight=1)
# window.columnconfigure(2, weight=1)
# window.rowconfigure(2, weight=1)