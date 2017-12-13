import os

import discord
import sys
from discord.ext import commands
import analyze


path = os.path.join(sys.path[0], "config.txt")

f = open(path)
token = ''
for line in f:
    if "DisBoxTockin:" in line:
        token = line.split("DisBoxTockin:")[1].strip()

f.close()

client = discord.Client()
bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready(*a):
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')



@bot.command(pass_context=True)
async def hey(ctx):

    member = ctx.message.author



    await bot.say('{0} you suck'.format(member.name))

@bot.command()
async def hello():

    await bot.say('#hello')


@bot.command()
async def dndStats(*args):
    await bot.say("getting data this may take moment")
    await bot.say(analyze.talk(*args))

@bot.command()
async def kill():
    await bot.say("I am deb")
    await bot.logout()

@bot.command()
async def helpme():
    await bot.say("To get total stats say \"$dndStats\" "
                  "\nTo get the most current Stats say \"$dndStats #\" # being the number hours you want to look back")




bot.run(token)


