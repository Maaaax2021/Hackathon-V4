from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC
import time

days=["Monday","Tuesday","Wednesday","Thursday","Friday"]

def ListToString(l):
  data=""
  for x in range(len(l)):
    data+=str(l[x])
  return data

def FormatStringTime(string_time,char):
  while True:
    try:
      string_time.remove(char)
    except ValueError:
      return string_time

def GetCombs(start_day):
  start_day=str(start_day)
  start_month="01"
  combs_for_day=[]
  for x in range(10):
    combs_for_day.append(str(start_month)+str(start_day))
    for counter in range(7):
      start_day=str(int(start_day)+1)
      if len(start_day)==1:
        start_day="0"+start_day
      if int(start_day) > 31 and int(start_month)!=2 or int(start_day) > 28 and int(start_month)==2:
        start_month=str(int(start_month)+1)
        if len(start_month)==1:
          start_month="0"+start_month
        start_day="01"
  return combs_for_day

def CheckDateIsDay(date,day):
  start_date=18+days.index(day)
  combs=GetCombs(start_date)
  return True if date in combs else False

def GetDay(string_time):
  s=list(string_time)
  s=FormatStringTime(s,"-")
  s=FormatStringTime(s,":")
  string_time=ListToString(s)
  monthdate=string_time[s.index(" ")-4:s.index(" ")]
  for day in days:
    if CheckDateIsDay(monthdate,day):
      break
  return day

def GetTime(string_time):
  s=list(string_time)
  s=FormatStringTime(s,"-")
  s=FormatStringTime(s,":")
  string_time=ListToString(s)
  return string_time[s.index(" ")+1:s.index(" ")+1+4]

def conv_day_event_to_dic(component,daytable):
  datetime_obj=component.decoded('dtstart')
  hour=GetTime(str(datetime_obj))
  lecture=component.decoded('summary').decode("utf-8")
  daytable.update({hour:lecture})
  return daytable

def conv_event_to_dic(component,timetable):
  day=GetDay(str(component.decoded('dtstart')))
  daytable=conv_day_event_to_dic(component,timetable[day] if timetable[day] is not None else {})
  timetable.update({day:daytable})
  return timetable

def conv_cal_to_dic(cal):
  timetable={day:None for day in days}
  with open(cal+'_timetable.ics','rb') as g:  #Using with auto closes even if there's an error
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
        if component.name == "VEVENT":
          timetable=conv_event_to_dic(component,timetable)
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
      daytable["1100"]=daytable["1100"].replace("1110","1120")
  return timetable
#timetable=FormatDic(conv_cal_to_dic())
# ~ for day,daytable in timetable.items():
  # ~ print(day,end=":\n")
  # ~ for k,v in daytable.items():
    # ~ print("  "+k+": "+v)
