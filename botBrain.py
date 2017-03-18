import discord
from discord.ext import commands
import main
import random

client = discord.Client()
bot = commands.Bot(command_prefix='#')


@bot.event
async def on_ready(*a):
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello():
    await bot.say("shut the fuck up")



@bot.command()
async def dndstuff():
    await bot.say(main.talk())

@bot.command()
async def kill():
    await bot.say("I am deb")
    await bot.logout()


bot.run('')


