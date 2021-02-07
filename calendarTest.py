from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC
import time

days=["Monday","Tuesday","Wednesday","Thursday","Friday"]

def ListToString(l):
  data=""
  for x in range(len(l)):
    data+=str(l[x]) #for turning a list back to a string
  return data

def FormatStringTime(string_time,char):
  while True: #remove until doesn't exist
    try:
      string_time.remove(char)
    except ValueError:
      return string_time #exit if non-existant

def GetCombs(start_day):
  start_day=str(start_day) #from the start day, return all day/month combinations
  start_month="01"
  combs_for_day=[]
  for x in range(10):
    combs_for_day.append(str(start_month)+str(start_day)) #in the form MMDD
    for counter in range(7):
      start_day=str(int(start_day)+1)
      if len(start_day)==1:
        start_day="0"+start_day
      if int(start_day) > 31 and int(start_month)!=2 or int(start_day) > 28 and int(start_month)==2:
        start_month=str(int(start_month)+1)
        if len(start_month)==1: #because conversion between str and int removes trailing 0s, format them back in
          start_month="0"+start_month
        start_day="01"
        #incr month if days exceed month length
  return combs_for_day

def CheckDateIsDay(date,day):
  start_date=18+days.index(day) #18/01 was Monday, find start day from day of week based on that monday
  combs=GetCombs(start_date)
  return True if date in combs else False

def GetDay(string_time):
  s=list(string_time)
  s=FormatStringTime(s,"-")
  s=FormatStringTime(s,":")
  string_time=ListToString(s)
  monthdate=string_time[s.index(" ")-4:s.index(" ")] #go up to space (gap between month and time) from first month digit to get MMDD format
  for day in days: #find what day it is
    if CheckDateIsDay(monthdate,day):
      break
  return day

def GetTime(string_time):
  s=list(string_time)
  s=FormatStringTime(s,"-")
  s=FormatStringTime(s,":")
  string_time=ListToString(s)
  return string_time[s.index(" ")+1:s.index(" ")+1+4] #go from space +1 (the first time digit) to the fourth time digit for HHMM

def conv_day_event_to_dic(component,daytable):
  datetime_obj=component.decoded('dtstart') #get decoded start
  hour=GetTime(str(datetime_obj))
  lecture=component.decoded('summary').decode("utf-8")
  daytable.update({hour:lecture}) #time is key, summary is value
  return daytable

def conv_event_to_dic(component,timetable):
  day=GetDay(str(component.decoded('dtstart')))
  daytable=conv_day_event_to_dic(component,timetable[day] if timetable[day] is not None else {})
  timetable.update({day:daytable}) #day is key, dictionary of hours and lectures is value
  return timetable

def conv_cal_to_dic(cal):
  timetable={day:None for day in days}
  with open(cal+'_timetable.ics','rb') as g:  #Using with auto closes even if there's an error
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
        if component.name == "VEVENT":
          timetable=conv_event_to_dic(component,timetable) # if event
  return timetable

def FormatDic(timetable):
  for day in days:
    daytable=timetable[day]
    if day=="Monday":
      if "EE1120" in daytable["1000"]:
        del daytable["1000"]
    elif day=="Tuesday":
      if "EE1030" in daytable["0900"]:
        del daytable["0900"]
    elif day=="Wednesday":
      daytable["0930"]=daytable["0900"]
      del daytable["0900"]
    elif day=="Friday":
      del daytable["1000"]
      del daytable["1300"]
      del daytable["0900"]
      del daytable["1200"]
      daytable["1400"]=daytable["1400"].replace("1020","1000")
      daytable["1400"]=daytable["1400"].replace("Online","Lab")
      daytable["1100"]=daytable["1100"].replace("1110","1120") #format old lecture data
  return timetable
