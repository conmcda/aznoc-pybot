import datetime

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime = secondsToText(uptime_seconds)

    return uptime

def secondsToText(secs):
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60
    result = ("{} days, ".format(int(days)) if days else "") + \
    ("{} hours, ".format(int(hours)) if hours else "") + \
    ("{} minutes, ".format(int(minutes)) if minutes else "") + \
    ("{} seconds, ".format(int(seconds)) if seconds else "")
    return result

def get_christmas(date):
    """Returns the date of the Christmas of the year of the date"""
    next_xmas = datetime.datetime(date.year, 12, 25)
    if next_xmas < date:
        next_xmas = datetime.datetime(date.year+1, 12, 25)
    return next_xmas

def days_to_xmas(input_date):
    ans = (get_christmas(input_date) - input_date).days
    return ans
