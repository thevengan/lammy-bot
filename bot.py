import discord
from discord.ext import commands

import os

token = "ODI0MDM2OTEyMjk2ODg2Mjgy.YFpiLQ.3TZPNFsZI-QyJ0aLojNxjU43vBA"
#token = os.getenv("DISCORD_BOT_TOKEN")

description = "TODO: Change Me"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

BOT_CHANNELS = ('bot-spam', 'spam-bot')

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------------")

@bot.command()
async def soainitialize(ctx):
    role_names = [role.name for role in ctx.guild.roles]
    if "sino_guerrilla" not in role_names:
        await ctx.guild.create_role(name="sino_guerrilla")
    if "sino_conquest" not in role_names:
        await ctx.guild.create_role(name="sino_conquest")
    if "sino_purification" not in role_names:
        await ctx.guild.create_role(name="sino_purification")

@bot.command()
async def soagiverole(ctx):
    if "guerrilla" in ctx.message.content:
        roles = [role for role in ctx.guild.roles if role.name == "sino_guerrilla"]
        for role in roles:
            await ctx.author.add_roles(role)
    if "conquest" in ctx.message.content:
        roles = [role for role in ctx.guild.roles if role.name == "sino_conquest"]
        for role in roles:
            await ctx.author.add_roles(role)
    if "purification" in ctx.message.content:
        roles = [role for role in ctx.guild.roles if role.name == "sino_purification"]
        for role in roles:
            await ctx.author.add_roles(role)

@bot.command()
async def soaremoverole(ctx):
    if "guerrilla" in ctx.message.content:
        roles = [role for role in ctx.guild.roles if role.name == "sino_guerrilla"]
        for role in roles:
            await ctx.author.remove_roles(role)
    if "conquest" in ctx.message.content:
        roles = [role for role in ctx.guild.roles if role.name == "sino_conquest"]
        for role in roles:
            await ctx.author.remove_roles(role)
    if "purification" in ctx.message.content:
        roles = [role for role in ctx.guild.roles if role.name == "sino_purification"]
        for role in roles:
            await ctx.author.remove_roles(role)

@bot.command()
async def whoami(ctx):
    await ctx.send(f"You are {ctx.message.author.name}")

if __name__ == "__main__":
    bot.run(token)