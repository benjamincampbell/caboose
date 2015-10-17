import os
import time
import datetime

def remindercheck(privmsg):
    #format: MM/DD/YYYY HH:MM nick reminder text
    currentdate = datetime.datetime.now()
    rm = open("reminders.txt", "r")
    reminderlist = rm.readlines()
    rm.close()

    rm = open("reminders.txt", "w")
    for line in reminderlist:
        
        #this bit here is messy, but i needed to extract the month, day,
        #year, hour, and minute from the reminder in the line to load
        #into the datetime object, to compare to the current datetime.
        try: 
            reminderdate, remindertime, remindernick, remindertext = line.split(' ', maxsplit = 3)
            remmonth, remday, remyear = reminderdate.split('/')
            remhour, remmin = remindertime.split(':')
            #get the difference between the reminder time and current time
            reminderobject = datetime.datetime(int(remyear), int(remmonth), int(remday), int(remhour), int(remmin))
            reminderdelta = reminderobject - currentdate
            #if it's less than 59 seconds, remind! if not, write it to file to keep for later
            if reminderdelta < datetime.timedelta(seconds = 1):
                print("Reminder detected!")
                print(reminderdelta)
                privmsg(remindernick, '{}: REMINDER: {}'.format(remindernick, remindertext))
            else:
                rm.write(line)
        except IndexError:
            print("Reminders file empty")

    rm.close()
    #Create and start a 60 second treading timer to do remindercheck
    print("Reminders Checked")