'''PFA-POS Alignment Traveler with Actual GUI

created by: Rohan Castelino
using work done by: gradeywang and a lot of googling
on: Thursday, June 28th, 2018
issues?: email rcastelino@lbl.gov

DESI at LBL is in the process of manufacturing over 10,000 positioners. Recently, technicians have been filling out a spreadsheet (of the same name as
this program) by hand to keep track of the progress of positioners currently being produced. To make things easier, this program was developed. It takes in
details about each positioner and updates a google sheet with this information. For more documentation about the workings of this program, its development
process or common errors that may arise, check out the README folder.
'''

#python setup
from tkinter import *
from PIL import ImageTk
from PIL import Image
from tkinter import ttk
import gspread
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
repeat_flag = 0
donebefore = 0
positionerIDcount = 0
y = 0
latestrow = 0
donotcontinue = 0
positionerIDints = []
positionerIDstrings = []
step0=0
step1=0
step2=0
notes = []


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
    global positionerIDtextbox,notestextbox
    positionerIDtextbox = Entry(positionerIDtextboxframe,width=10)
    positionerIDtextbox.grid(column=1,row=0)
    notestextbox = Entry(positionerIDtextboxframe,width=10)
    notestextbox.grid(column=1,row=1)

#functions to modify widgets
def infotextboxOverwriting(step,name,date):
    global donebefore, givensteplabel,givennamelabel,givendatelabel
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

def positionerIDsgivenlabels(positionerID,positionerIDcount):
    global y
    if positionerIDcount < 5:
        x = 1
    elif 5 <= positionerIDcount < 10:
        x = 2
    elif 10 <= positionerIDcount < 15:
        x = 3
    elif 15 <= positionerIDcount < 20:
        x = 4
    elif positionerIDcount == 20:
        x = 0

    IDlabel = Label(IDlistframe, text=positionerID, font=("Arial,12"))
    IDlabel.grid(column=x, row=y)

    if positionerIDcount ==20:
        y=-1
    if y == 4:
        y = 0
    else:
    	y = y + 1

#operation functions
def infobuttonclicked():
    global positionerIDints,positionerIDstrings,notes,step,name,date
    step = steptextbox.get()
    name = nametextbox.get()
    date = datetextbox.get()
    infovalidation(step,name,date)
    if validationstatus == 3:
        infotextboxOverwriting(step, name, date)
        positionerIDtextbox.focus()
#        printtoconsole('Info valid.')
        infoprocessing(step)

        positionerIDints = []
        positionerIDstrings = []
        notes = []

def positionerIDbuttonclicked():
    global donotcontinue
    global positionerIDcount,IDlistframe,notes,positionerIDtextbox
    positionerID = positionerIDtextbox.get()
    note = notestextbox.get()
    try:
        val = int(positionerID)
    except ValueError:
        printtoconsole("Not a valid positionerID!")
        donotcontinue = 1
    if donotcontinue == 0:
        positionerID = positionerID.lstrip('0')
        positionerIDstrings.append(positionerID)
        positionerID = int(positionerID)
        positionerIDints.append(positionerID)
        notes.append(note)
        positionerIDtextbox.grid_remove()
        if positionerIDcount == 0:
            IDlistframe = Frame(window)
            IDlistframe.grid(column=2,row=2)
            positionerIDsgivenlabels("Positioner IDs already scanned:",20)
        if positionerIDcount == 19:
            positionerIDsgivenlabels(positionerID,positionerIDcount)
            infotextboxSetup()
            steptextbox.focus()
            positionerIDcount = 0
        else:
            positionerIDsgivenlabels(positionerID,positionerIDcount)
            positionerIDcount = positionerIDcount + 1
        positionerIDtextbox = Entry(positionerIDtextboxframe,width=10)
        positionerIDtextbox.grid(column=1,row=0)
        positionerIDtextbox.focus()

def continueButtonclicked():
    global positionerIDstrings,positionerIDints,name,date,step,notes,positionerIDcount
    #printtoconsole('Writing...')
    for i1 in range(len(positionerIDints)):
        existing_cell_value = ''
        printtoconsole('Updated information for Positioner ' + positionerIDstrings[i1])

        values_list_raw = wks.col_values(1)
        length = len(values_list_raw)
        values_list = [values_list_raw[i2] for i2 in range(3,length)]
        values_list_int = list(map(int, values_list))

        if positionerIDstrings[i1] in values_list:
            serial_number = positionerIDints[i1]
            decided_cell_row = np.asscalar(np.int16(np.searchsorted(values_list_int, serial_number, side='right') + 3))
            decided_cell0 = step0 + str(decided_cell_row)
            existing_cell_value = wks.acell(decided_cell0).value
            if existing_cell_value != '':
                printtoconsole("***Existing information for this positioner already! Possible anomaly on spreadsheet. Sheet not updated.***")
                continue
        else:
            serial_number = positionerIDints[i1]
            decided_cell_row = np.asscalar(np.int16(np.searchsorted(values_list_int, serial_number, side='right') + 4))
            wks.insert_row([serial_number],decided_cell_row)
            decided_cell0 = step0 + str(decided_cell_row)

        decided_cell1 = step1 + str(decided_cell_row)
        decided_cell2 = step2 + str(decided_cell_row)

        wks.update_acell(decided_cell0, name)
        wks.update_acell(decided_cell1, date)
        wks.update_acell(decided_cell2, notes[i1])

        infotextboxSetup()
        steptextbox.focus()
    positionerIDcount = 0
    printtoconsole("Finished writing.")
    IDlistframe.destroy()

#dictionary for converting number to column number
def f(x):
    return {
        '1': 'A',
        '2': 'B',
        '3': 'C',
        '4': 'D',
        '5': 'E',
        '6': 'F',
        '7': 'G',
        '8': 'H',
        '9': 'I',
        '10': 'J',
        '11': 'K',
        '12': 'L',
        '13': 'M',
        '14': 'N',
        '15': 'O',
        '16': 'P',
        '17': 'Q',
        '18': 'R',
        '19': 'S',
        '20': 'T',
        '21': 'U',
        '22': 'V',
        '23': 'W',
        '24': 'X',
        '25': 'Y',
        '26': 'Z',
        '27': 'AA',
        '28': 'AB',
        '29': 'AC',
        '30': 'AD',
        '31': 'AE',
    }[x]

#dictionary for converting step string to number can use
steps =  {
    'Cut fiber': '2',
    'Installed hytrel': '5',
    'Bonded hardpoint': '8',
    'Installed clip': '11',
    'Installed furcation': '14',
    'Moved to holster': '17',
    'Epoxied clip': '20',
    'Confirmed epoxy curing': '23',
    'Tape removed': '26',
    'QA check': '29',
}

def infovalidation(step,name,date):
    global validationstatus
    stepApproved = 0
    nameApproved = 0
    dateApproved = 0
    if step in steps:
        stepApproved = 1
    else:
        printtoconsole('Not a valid step!')
    if name != '':
        nameApproved = 1
    else:
        printtoconsole('Not a valid name!')
    if name[0].lower() == name[0]:
        name = name.swapcase()
    if date != '':
        dateApproved = 1
    else:
        printtoconsole('Not a valid date!')
    validationstatus = stepApproved + nameApproved + dateApproved
    return validationstatus


def printtoconsole(stringtoprint):
    global latestrow
    Label(consoleFrame,text=stringtoprint, font=('Arial',10)).grid(column=0,row=latestrow)
    latestrow = latestrow + 1

def infoprocessing(step):
    global step0,step1,step2
#math to get multiple columns
    step0 = steps[step]
    step0int = int(step0)
    step1int = step0int + 1
    step2int = step0int + 2

#converts to string to check in dictionary
    step1 = str(step1int)
    step2 = str(step2int)

#finds correct column string for indexing cell
    step0 = f(step0)
    step1 = f(step1)
    step2 = f(step2)


#gui setup
window = Tk()
window.title("PFA-POS Alignment Traveler Updates")
window.geometry('785x500')


#image setup
backdropimg = Image.open("backdrop.jpg")
logo = Image.open("logo.jpg")
logo = logo.resize((100,80), Image.ANTIALIAS)
backdropimg.paste(logo, (50, 50))
backdropimg = ImageTk.PhotoImage(backdropimg)
backdrop = Label(window, image=backdropimg, text="PFA-POS Alignment Traveler Updates", fg="white", font=("Calibri",30), compound=CENTER)
backdrop.grid(column=0, row=0, columnspan=3)
backdrop.image = backdropimg


#Frame setup
infoFrame = Frame(window)
infoFrame.grid(column=0,row=1)
verticalline = ttk.Separator(window,orient=VERTICAL)
verticalline.grid(column=1,row=1,rowspan=2,sticky="ns")
positionerIDtextboxframe = Frame(window)
positionerIDtextboxframe.grid(column=2,row=1)
IDlistframe = Frame(window)
IDlistframe.grid(column=2,row=2)
horizontalline = ttk.Separator(window,orient=HORIZONTAL)
horizontalline.grid(column=0,row=3,columnspan=11,sticky="ew")
consoleFrame = Frame(window)
consoleFrame.grid(column=0,row=4,columnspan=3)
consolescrollbar = Scrollbar(consoleFrame)
consolescrollbar.grid


#info input
steplabel = Label(infoFrame, text="Step:", font=("Arial", 16))
steplabel.grid(column=0, row=0)
namelabel = Label(infoFrame, text="Name:", font=("Arial", 16))
namelabel.grid(column=0, row=1)
datelabel = Label(infoFrame, text="Date:", font=("Arial", 16))
datelabel.grid(column=0, row=2)
infobutton = Button(infoFrame, text="Enter", bg="white", font=("Calibri",10), command=infobuttonclicked)
infobutton.grid(column=1, row=3)



#ID input
positionerIDlabel = Label(positionerIDtextboxframe, text="Positioner ID:", font=("Arial", 16))
positionerIDlabel.grid(column=0, row=0)
positionerIDbutton = Button(positionerIDtextboxframe, text="Enter", bg="white", font=("Calibri",10), command=positionerIDbuttonclicked)
positionerIDbutton.grid(column=1, row=2)
notesLabel = Label(positionerIDtextboxframe, text="Any notes?:", font=("Arial", 16))
notesLabel.grid(column=0, row=1)
continueButton = Button(positionerIDtextboxframe, text="Continue", bg="white", font=("Calibri",10), command=continueButtonclicked)
continueButton.grid(column=1, row=3)



#preps sheet access for use
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('PFA-POS Alignment Traveler-11563768dd12.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_url('hittps://docs.google.com/spreadsheets/d/1x2XhO7uQna9g_p_IA8FshYEVjCgG6mpxJjpODoLzRBs/edit#gid=1383770368').sheet1



#console setup
printtoconsole('Hi! This program helps track of the progress of positioners and updates the PFA-POS Alignment Traveler spreadsheet.')

#Operation
infotextboxSetup()
positionerIDtextboxSetup()
window.mainloop()
