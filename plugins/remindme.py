import datetime
def remindme(nick, channel, message, privmsg):
    #Structure is nick channel MM/DD/YYYY HH:MM reminder

    #split the message into parts
    try:
        remdate, remtime, remtext = message.split(maxsplit = 2)
    except:
        dateformat = False
    #split the date into parts
    try:
        dateyear, datemonth, dateday = remdate.split('/')
        dateformat = True
    except:
        dateformat = False #IndexError means less than 2 splits were made, which means a character other than '/' was used to split.

    #split the time into parts
    try:
        timehr, timemin = remtime.split(':')
        timeformat = True
    except:
        timeformat = False #IndexError means less than 1 split was made, which means a character other than ':' was used to split

    def checkdate(string): #function to check date format
        try:
            datetime.datetime.strptime(string, '%Y/%m/%d')
            format = True
        except:
            format = False

        #we also need to make sure the date hasn't already passed
        if timeformat and dateformat:
            currentdate = datetime.datetime.now()#datetime object holding the current date and time
            reminderdate = datetime.datetime(int(dateyear), int(datemonth), int(dateday), int(timehr), int(timemin))#datetime object holding the reminder date and time

            if reminderdate >= currentdate: #if reminder date/time is same or further in future than current date and time
                if format == True: #and if the format of the date/time is correct as well
                    return True #the date format checks out, all is well.
                else:
                 pass
            else: #if reminder date/time is before the current date time, no point in setting a reminder.
                privmsg(channel, '{}: {}'.format(nick, "Please enter a date that has not passed."))
                return False
        else:
            privmsg(channel, '{}: {}'.format(nick, "Please use <<&remindme MM/DD/YYYY HH:MM reminder text>> format."))

    def checktime(string):#function to check time format
        try:
            datetime.datetime.strptime(string, '%H:%M')
            return True
        except ValueError:
            privmsg(channel, '{}: {}'.format(nick, "Please use 24 hour HH:MM format."))
    try:
        if checkdate(remdate) and checktime(remtime):
            rm = open("reminders.txt", "a")
            rm.write(remdate + " " + remtime + " " + nick + " " + remtext)
            rm.close()
            privmsg(channel, '{}: {}'.format(nick, "Reminder set for " + remdate + " at " + remtime + "."))
    except:
        pass