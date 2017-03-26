import os

import discord
import sys
from discord.ext import commands
import analyze
import random


path = os.path.join(sys.path[0], "E:\\GitProjects\\roll20Analyzer\\botConfig")

f = open(path)
confg = f.read()
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
async def now():
    await bot.say("ok sorry")



@bot.command()
async def dndstuff(*args):
    await bot.say("getting data this may take moment")
    await bot.say(analyze.talk(*args))

@bot.command()
async def kill():
    await bot.say("I am deb")
    await bot.logout()


bot.run(confg)


