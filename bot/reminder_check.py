import os
import time
import datetime
import threading

def remindercheck(privmsg):
    #format: MM/DD/YYYY HH:MM nick reminder text
    currentdate = datetime.datetime.now()
    rm = open("reminders.txt", "r")
    reminderlist = rm.readlines()
    rm.close()

    rm = open("reminders.txt", "w")
    for line in reminderlist:
        reminder = line.split(' ', maxsplit = 3)
        #this bit here is messy, but i needed to extract the month, day,
        #year, hour, and minute from the reminder in the line to load
        #into the datetime object, to compare to the current datetime.
        reminderdate = reminder[0]
        remindertime = reminder[1]
        remindernick = reminder[2]
        remindertext = reminder[3]
        
        reminderdatesplit = reminderdate.split('/')
        remmonth = reminderdatesplit[0]
        remday = reminderdatesplit[1]
        remyear = reminderdatesplit[2]

        remindertimesplit = remindertime.split(':')
        remhour = remindertimesplit[0]
        remmin = remindertimesplit[1]
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
    rm.close()
    #Create and start a 60 second treading timer to do remindercheck
    t = threading.Timer(60.0, remindercheck)
    t.daemon = True
    t.start()
    print("Reminders Checked")