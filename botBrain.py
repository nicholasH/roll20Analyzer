import discord
from discord.ext import commands
import main
import random

client = discord.Client()
bot = commands.Bot(command_prefix='D&D_NPC_BOT')


@bot.event
async def on_ready(*a):
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello():
    await bot.say("fuck you")

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))


@bot.command()
async def dndstuff():
    await bot.say(main.talk())


bot.run('MjIxNDEyNjc3MzAwMzg3ODQw.CqvEvA._JQkxIDtrCDpMxHUoLj4cqV1I54')