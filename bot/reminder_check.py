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
        try: 
            #get all of our time-related data from the reminder line
            reminderdate, remindertime, remindernick, remindertext = line.split(' ', maxsplit = 3)
            #remmonth, remday, remyear = reminderdate.split('/')
            #remhour, remmin = remindertime.split(':')
            #get the difference between the reminder time and current time
            reminderobject = datetime.datetime(*[int(x) for x in reminderdate.split('/')] + [int(x) for x in remindertime.split(':')])
            reminderdelta = reminderobject - currentdate
            #if it's less than 59 seconds, remind! if not, write it to file to keep for later
            if reminderdelta < datetime.timedelta(seconds = 1):
                print("Reminder detected!")
                print(reminderdelta)
                privmsg(remindernick, '{}: REMINDER: {}'.format(remindernick, remindertext))
            else:
                rm.write(line)
        except ValueError:
            print("Reminders file empty")
    rm.close()
    print("Reminders Checked")