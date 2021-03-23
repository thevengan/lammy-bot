import discord
from discord.ext import commands
import os

token = os.getenv("DISCORD_BOT_TOKEN")

description = "TODO: Change Me"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------------")

@bot.command()
async def whoami(ctx):
    await ctx.send(f"You are {ctx.message.author.name}")

bot.run(token)