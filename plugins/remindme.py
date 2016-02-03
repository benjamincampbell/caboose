

@command("remindme", man = "Sets a reminder at a given time to be private messaged to you. Usage: &remindme YYYY/MM/DD HH:MM 'reminder text', please use 24-hour time format")
def remindme(nick, channel, message, handler):
    import datetime
    #Structure is nick channel MM/DD/YYYY HH:MM reminder

    def checkdate(): #function to check date
        currentdate = datetime.datetime.now()#datetime object holding the current date and time
        reminderdate = datetime.datetime(*[int(x) for x in remdate.split('/')] + [int(x) for x in remtime.split(':')])#datetime object holding the reminder date and time

        if reminderdate >= currentdate: #if reminder date/time is same or further in future than current date and time
            return True #the date format checks out, all is well.
        else: #if reminder date/time is before the current date time, no point in setting a reminder.
            handler.privmsg(channel, '{}: {}'.format(nick, "Please enter a date that has not passed."))#friendly note
            return False

    try:
        remdate, remtime, remtext = message.split(maxsplit = 2)
        if checkdate():
            rm = open("reminders.txt", "a")
            rm.write(remdate + " " + remtime + " " + channel + " " + nick + " " + remtext + "\n")
            rm.close()
            handler.privmsg(channel, '{}: {}'.format(nick, "Reminder set for " + remdate + " at " + remtime + "."))
    except ValueError: #This should catch any improper date formatting that happens when it tries to create the datetime object
        handler.privmsg(channel, '{}: {}'.format(nick, "Please use <<&remindme YYYY/MM/DD HH:MM reminder text>> format."))