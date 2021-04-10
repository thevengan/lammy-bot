import discord
from discord.ext import commands, tasks

import os
from datetime import time, datetime
from schedules import GUERRILLA_TIMES, CONQUEST_TIMES, PURIFICATION_TIMES

token = os.getenv("DISCORD_BOT_TOKEN")

description = "TODO: Change Me"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

BOT_CHANNELS = ('bot-spam', 'spam-bot')

@tasks.loop(minutes=1)
async def ping_role():
    current_time = time(datetime.now().hour, datetime.now().minute)

    if current_time in GUERRILLA_TIMES:
        for guild in bot.guilds:
            channels = [channel for channel in guild.channels if channel.name in ('bot-spam', 'spam-bot')]
            role = [role for role in guild.roles if role.name == "sino_guerrilla"][0]

            for channel in channels:
                await channel.send(f"{role.mention}: Guerrilla is open for the next 30 minutes!")
    
    if current_time in CONQUEST_TIMES:
        for guild in bot.guilds:
            channels = [channel for channel in guild.channels if channel.name in ('bot-spam', 'spam-bot')]
            role = [role for role in guild.roles if role.name == "sino_conquest"][0]

            for channel in channels:
                await channel.send(f"{role.mention}: Conquest is open for the next 30 minutes!")

    if current_time in PURIFICATION_TIMES:
        for guild in bot.guilds:
            channels = [channel for channel in guild.channels if channel.name in ('bot-spam', 'spam-bot')]
            role = [role for role in guild.roles if role.name == "sino_purification"][0]

            for channel in channels:
                await channel.send(f"{role.mention}: Time to purify! Get that room clean!")   

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------------")

    print("Starting tasks")
    ping_role.start()
    print("Tasks started")
    print("------------")

    await bot.change_presence(activity=discord.Game(name="!soahelp"))

@bot.command()
async def soahelp(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        embed=discord.Embed(title="lammy-bot", description="The following are currently implemented commands for lammy-bot:")
        embed.add_field(name="Prefix", value="!soa", inline=True)        
        embed.add_field(name="initialize", value="Sets up the necessary roles and channels for users to interact with lammy-bot.", inline=False)
        embed.add_field(name="giverole", value="Gives the user a role(s). Accepts the following: guerrilla, conquest, purification.", inline=False)
        embed.add_field(name="removerole", value="Removes a role(s) from the user. Accepts the following: guerrilla, conquest, purification.", inline=False)
        await ctx.author.send(embed=embed)

@bot.command()
async def soainitialize(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        channel_names = [channel.name for channel in ctx.guild.channels]

        channels_added = []
        if "bot-spam" not in channel_names:
            await ctx.guild.create_text_channel(name="bot-spam")
            channels_added.append("bot-spam")

        role_names = [role.name for role in ctx.guild.roles]

        roles_added = []
        if "sino_guerrilla" not in role_names:
            await ctx.guild.create_role(name="sino_guerrilla")
            roles_added.append("sino_guerrilla")
        if "sino_conquest" not in role_names:
            await ctx.guild.create_role(name="sino_conquest")
            roles_added.append("sino_conquest")
        if "sino_purification" not in role_names:
            await ctx.guild.create_role(name="sino_purification")
            roles_added.append("sino_purification")

        if channels_added:
            await ctx.channel.send(f"{ctx.author.mention}: Created the following channel - {channels_added}.")
        else:
            await ctx.channel.send(f"{ctx.author.mention}: 'bot-spam' channel already exists.")
        if roles_added:
            await ctx.channel.send(f"{ctx.author.mention}: Created the following roles - {roles_added}.")
        else:
            await ctx.channel.send(f"{ctx.author.mention}: Roles already exist.")

@bot.command()
async def soagiverole(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        roles_added = []

        if "guerrilla" in ctx.message.content:
            roles = [role for role in ctx.guild.roles if role.name == "sino_guerrilla"]
            user_roles = [role for role in ctx.author.roles]
            for role in roles:
                if role not in user_roles:
                    await ctx.author.add_roles(role)
                    roles_added.append("sino_guerrilla")
        if "conquest" in ctx.message.content:
            roles = [role for role in ctx.guild.roles if role.name == "sino_conquest"]
            user_roles = [role for role in ctx.author.roles]
            for role in roles:
                if role not in user_roles:
                    await ctx.author.add_roles(role)
                    roles_added.append("sino_conquest")
        if "purification" in ctx.message.content:
            roles = [role for role in ctx.guild.roles if role.name == "sino_purification"]
            user_roles = [role for role in ctx.author.roles]
            for role in roles:
                if role not in user_roles:
                    await ctx.author.add_roles(role)
                    roles_added.append("sino_purification")

        if roles_added:
            await ctx.channel.send(f"{ctx.author.mention}: You've been given the following role(s) - {roles_added}.")
        else:
            await ctx.channel.send(f"{ctx.author.mention}: You're already in that role(s).")

@bot.command()
async def soaremoverole(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        roles_removed = []

        if "guerrilla" in ctx.message.content:
            roles = [role for role in ctx.guild.roles if role.name == "sino_guerrilla"]
            for role in roles:
                await ctx.author.remove_roles(role)
                roles_removed.append("sino_guerrilla")
        if "conquest" in ctx.message.content:
            roles = [role for role in ctx.guild.roles if role.name == "sino_conquest"]
            for role in roles:
                await ctx.author.remove_roles(role)
                roles_removed.append("sino_conquest")
        if "purification" in ctx.message.content:
            roles = [role for role in ctx.guild.roles if role.name == "sino_purification"]
            for role in roles:
                await ctx.author.remove_roles(role)
                roles_removed.append("sino_purification")

        if roles_removed:
            await ctx.channel.send(f"{ctx.author.mention}: You've been removed from the following role(s) - {roles_removed}.")
        else:
            await ctx.channel.send(f"{ctx.author.mention}: You're not a part of that role(s).")

@bot.command()
async def whoami(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        await ctx.send(f"You are {ctx.message.author.name}")

if __name__ == "__main__":
    bot.run(token)
