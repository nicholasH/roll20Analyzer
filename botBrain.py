import discord
from discord.ext import commands
import main
import random

client = discord.Client()
bot = commands.Bot(command_prefix='D&D')


@bot.event
async def on_ready(*a):
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello():
    await bot.say("fuck you")



@bot.command()
async def dndstuff():
    await bot.say(main.talk())


bot.run('MjIxNDEyNjc3MzAwMzg3ODQw.CqvEvA._JQkxIDtrCDpMxHUoLj4cqV1I54')