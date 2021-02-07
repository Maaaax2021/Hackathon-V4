import discord
from discord.ext import commands
import random
from time import gmtime as get_t, asctime as rep_t
import calendarTest as CT
import asyncio

channelID = 796797478820380675
BotToken = 'ODA'+'3Mjk1NTY'+'5MzAyNjUwODkw'
BotToken+='.YB16lg.JDqwpV'
BotToken+='-4cAju0yIQmA-'+'cLyhSX70'
days=["Monday","Tuesday","Wednesday","Thursday","Friday"]
users=[]
prefix="$"

class User:
    def __init__(self, disc_id, schl_id, timetable):
        temp_id = disc_id.split("#")
        self.strname = temp_id[0] #name to call them
        self.callname = disc_id #discord name + # + discriminator
        self.logon = schl_id #abcd123
        self.timetable = timetable
        self.call = None
        self.lesson=False #has lesson?


class TimeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, intents=discord.Intents.all(), command_prefix=prefix, **kwargs) #all permissions, can change prefix if needed
        self.task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(self.user.name, "is online")

    async def my_background_task(self):
      await self.wait_until_ready()
      channel = self.get_channel(channelID)
      guild = channel.guild
      members = guild.members
      for User in users:
        for member in members:
          if member.name == self.user.name:
            continue #not bot
          if member.name == User.strname: #check if discord User istance has same name as User object made here
            User.call = member.mention #make the call variable the string used to mention them
            break
      c_sec,c_min,c_hour,c_wday=GetTime() 
      while c_sec!=0: #if not directly on minute
          await asyncio.sleep(0.5) 
          c_sec,c_min,c_hour,c_wday=GetTime() #re-check
      while c_min != 27 and c_min != 57: #if not 3 minutes before a lecture
          await asyncio.sleep(60)
          c_sec,c_min,c_hour,c_wday=GetTime() #recheck
      for user in users: 
        for day, daytable in user.timetable.items(): #iterate through users checking day by day
          if c_wday == days.index(day): #check days are correct
            for hour, lesson in daytable.items():
              _hour = int(str(hour)[0:2])
              _min = int(str(hour)[2:])
              if c_min==27 and _hour==c_hour or c_min==57 and _hour==c_hour+1: #check current minute and '3 minutes before' case line up
                await channel.send("{1} You have a {0} lecture in 3 minutes!".format(lesson, user.call))
                user.lesson=True #say they have a lesson
      await asyncio.sleep(60*4) #wait 4 minutes (1 minute into lecture)
      for user in users:
        if user.lesson: #if they have a lesson
          await channel.send("{0} This is an attendance reminder!".format(user.call))
          user.lesson=False #remind to do attendance and say they no longer have one
      await asyncio.sleep(60*26) #sleep for 26 minutes (to make 30)

def MakeUser(disc_name,filename):
    f=filename.split("_") #get list of abcd123, then timetable
    school=f[0] #abcd123
    users.append(User(disc_name,school,CT.FormatDic(CT.conv_cal_to_dic(school)))) #create User object

def GetTime():
    obj = get_t()
    c_sec = obj.tm_sec
    c_min = obj.tm_min
    c_hour = obj.tm_hour
    c_wday = obj.tm_wday
    return c_sec,c_min,c_hour,c_wday #get current time, then return seconds, minute, hour (24h format), and weekday index (monday is the first day, has index 0)
