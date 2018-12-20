'''PFA-POS Alignment Traveler'''
'''
created by: Rohan Castelino
using work done by: gradeywang and a lot of googling
on: Friday June 15th, 2018
issues?: email rcastelino@lbl.gov

DESI at LBL is in the process of manufacturing over 10,000 positioners. Recently, technicians have been filling out a spreadsheet (of the same name as
this program) by hand to keep track of the progress of positioners currently being produced. To make things easier, this program was developed. It takes in 
details about each positioner and updates a google sheet with this information. For more documentation about the workings of this program, its development 
process or common errors that may arise, check out the README folder.
'''

print()
print('Hi! This program helps track of the progress of positioners and updates the PFA-POS Alignment Traveler spreadsheet.')
print('Loading...')
print()

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

#setup
import gspread
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
repeat_flag = 0

#preps sheet access for use
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('PFA-POS Alignment Traveler-11563768dd12.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_url('hittps://docs.google.com/spreadsheets/d/1x2XhO7uQna9g_p_IA8FshYEVjCgG6mpxJjpODoLzRBs/edit#gid=1383770368').sheet1 

while True:
#setup
    step_needed = 1
    name_needed = 1
    date_needed = 1

#begins gathering data via prompts
    if repeat_flag != 1:
        while step_needed != 0: 
            step0original = input('Please scan step: ')
            if step0original in steps:
                step_needed = 0
            else:
                print('Not a valid step!')
        while name_needed != 0: 
            name = input('Please scan your name: ')
            if name != '':
                name_needed = 0
            else:
                print('Not a valid name!')
        if name[0].lower() == name[0]:
            name = name.swapcase()
        while date_needed != 0: 
            date = input('Please scan date: ')
            if date != '':
                date_needed = 0
            else:
                print('Not a valid name!')
        print()

#math to get multiple columns
    step0 = steps[step0original]
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

#serial number gathering
    positionerIndex = []
    positionerIDints = []
    positionerIDstrings = []
    notes = []
    index = 0
    firstScan = True
    while True:    
        if not firstScan:
            positionerID = input('Please scan the next positioner prepped by ' + name + ' on ' + date + ' or hit enter to end: ')
        else:
            positionerID = input('Please scan the first positioner prepped by ' + name + ' on ' + date + ': ')
            firstScan = False
        if not positionerID:
            break
        try:
            val = int(positionerID)
        except ValueError:
            print("Not a valid positionerID!")
            continue
        anyNotes = input('Any notes? (Hit Enter if none): ')
#processing data gathered
        positionerID = positionerID.lstrip('0')
        positionerIDstrings.append(positionerID)
        positionerID = int(positionerID)
        positionerIDints.append(positionerID)
        notes.append(anyNotes)
        
    print()
    print('Writing...')

#pushing data to spreadsheet
    for i1 in range(len(positionerIDints)):
        existing_cell_value = ''
        print('Updating information for Positioner ' + positionerIDstrings[i1])
        
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
                print("***Existing information for this positioner already! Possible anomaly on spreadsheet. Sheet not updated.***")
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

    print('Finished writing!')
    print()

    repeat_flag = 0
    anotherRound = input('Scan another batch? Enter "y" to continue, "c" to continue with the same step/person/date or anything else to end: ')
    if anotherRound.lower() == 'c':
    	repeat_flag = 1
    elif not anotherRound.lower() == 'y':
        break