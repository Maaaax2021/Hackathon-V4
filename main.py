import discord
from discord.ext import commands
import random
import sendmessage as SM
from discord.utils import get

bot=SM.TimeBot()

def embed_pagesCreate():
  page1 = discord.Embed (
    title = 'Click here to download your timetable...',
    url = "https://webtimetables.royalholloway.ac.uk/",
    description = '... and attach it as a reply "\n" Done? React: thumbsup: to your attachment',
    colour = discord.Colour.orange()
  )
  page2 = discord.Embed (
      title = 'Valid',
      description = 'Timetable Acknowledged',
      colour = discord.Colour.green()
  )
  page3 = discord.Embed (
      title = 'Invalid',
      description = 'Timetable must be in the format ABCD123_timetable.ics',
      colour = discord.Colour.red()
  )
  pages = [page1, page2, page3]
  return pages


@bot.command()
async def timetable(message):
  pages = embed_pagesCreate()

  if message.author == bot.user:
    return
  await message.author.create_dm()
  await message.author.dm_channel.send(embed=pages[0])


@bot.event
async def on_reaction_add(reaction, user):
  pages = embed_pagesCreate()

  if reaction.emoji == '👍':
    message = discord.utils.get(await user.dm_channel.history(limit=3).flatten(), author=user)

    try: ##If they don't send a message and just react to the messages sent
      msg_attachment=message.attachments
      if len(msg_attachment) > 0:
        for attachment in msg_attachment:
          if attachment.filename.endswith(".ics") and attachment.filename.find("_") == 7: #index of _ should be 7
            pages = embed_pagesCreate()
            await attachment.save(attachment.filename)
            SM.MakeUser(message.author.name+"#"+message.author.discriminator,attachment.filename) #make user and send valid page

            await message.author.dm_channel.send(embed=pages[1]) #valid?
          else:
            await message.author.dm_channel.send(embed=pages[2]) #invalid?

    except AttributeError:
      await user.dm_channel.send(embed=pages[2]) #invalid?

bot.run(SM.BotToken)
