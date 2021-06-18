# discord import
import discord
from discord import Embed
from discord.ext import commands, tasks

# default library imports
import os
import requests
import json
from datetime import time, datetime

# non default imports
from sqlalchemy import and_
from sqlalchemy.log import instance_logger

# local imports
from schedules import GUERRILLA_TIMES, CONQUEST_TIMES, PURIFICATION_TIMES
from models import Card, CardEvolution, Item, Skill, LimitBreakSkill, Character, CharacterAbility
from crud import recreate_database, populate_database, session_scope
from constants import BOT_CHANNELS, IMAGE_URL, VERSION_URL

# set the discord bot token
token = os.getenv("DISCORD_BOT_TOKEN")

description = "TODO: Change Me"

intents = discord.Intents.default()
intents.members = True

# instantiate bot
bot = commands.Bot(command_prefix='!', description=description, intents=intents)

# ping_role task that acts every minute and pings applicable roles
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

@tasks.loop(hours=1)
async def update_db():
    datamine_version = requests.get(VERSION_URL).json()["lastCreatedTime"]
    date_part = datamine_version.split(" ")[0]
    time_part = datamine_version.split(" ")[1]

    year_part = int(date_part.split("-")[0])
    month_part = int(date_part.split("-")[1])
    day_part = int(date_part.split("-")[2])

    hour_part = int(time_part.split(":")[0])
    minute_part = int(time_part.split(":")[1])
    second_part = int(time_part.split(":")[2])

    datamine_updated = datetime(
        year=year_part,
        month=month_part,
        day=day_part,
        hour=hour_part,
        minute=minute_part,
        second=second_part
    )

    current_version = None
    with open("version.json", "r") as version:
        current_version = json.load(version)["lastUpdatedTime"]

    date_part = current_version.split(" ")[0]
    time_part = current_version.split(" ")[1]

    year_part = int(date_part.split("-")[0])
    month_part = int(date_part.split("-")[1])
    day_part = int(date_part.split("-")[2])

    hour_part = int(time_part.split(":")[0])
    minute_part = int(time_part.split(":")[1])
    second_part = int(time_part.split(":")[2])

    last_updated = datetime(
        year=year_part,
        month=month_part,
        day=day_part,
        hour=hour_part,
        minute=minute_part,
        second=second_part
    )

    if datamine_updated > last_updated:
        recreate_database()
        populate_database()

# standard startup
@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------------")

    print("Starting tasks")
    ping_role.start()
    update_db.start()
    print("Tasks started")
    print("------------")

    await bot.change_presence(activity=discord.Game(name="!soahelp"))

# help command - sends a DM to the caller
@bot.command()
async def soahelp(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        embed=discord.Embed(title="lammy-bot", description="The following are currently implemented commands for lammy-bot:")
        embed.add_field(name="Prefix", value="!soa", inline=True)        
        embed.add_field(name="initialize", value="Sets up the necessary roles and channels for users to interact with lammy-bot.", inline=False)
        embed.add_field(name="giverole", value="Gives the user a role(s). Accepts the following: guerrilla, conquest, purification.", inline=False)
        embed.add_field(name="removerole", value="Removes a role(s) from the user. Accepts the following: guerrilla, conquest, purification.", inline=False)
        await ctx.author.send(embed=embed)

# initialize command - sets up necessary channels and roles
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

# giverole command - gives the specified role(s) to the caller
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

# removerole command - removes the specified role(s) from the caller
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

# weapon command - queries the db and display information about the requested weapon
@bot.command()
async def soaweapon(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        weapon_name = ctx.message.content[11:]

        with session_scope() as s:
            weapon = s.query(Card).filter(and_(Card.name.ilike(f'%{weapon_name}%'), Card.evolutionLevel==0)).first()

            if weapon is None:
                await ctx.channel.send(f"{ctx.author.mention}: I couldn't find a weapon matching {weapon_name}. Please try again.")
                return

            story_skill = s.query(Skill).filter(Skill.skillMstId==weapon.questSkillMstId).first()
            colo_skill = s.query(Skill).filter(Skill.skillMstId==weapon.frontSkillMstId).first()
            colo_supp_skill = s.query(Skill).filter(Skill.skillMstId==weapon.autoSkillMstId).first()

            color = 0x000000
            if weapon.attribute == 1:
                color = 0xFF0000
            elif weapon.attribute == 2:
                color = 0x0000FF
            elif weapon.attribute == 3:
                color = 0x00FF00

            rarity = "A"
            if weapon.rarity == 4:
                rarity = "S"
            elif weapon.rarity == 5:
                rarity = "SR"
            elif weapon.rarity == 6:
                rarity = "L"

            infinity_weapon = "NO"
            if weapon.isInfiniteEvolution:
                infinity_weapon = "YES"

            skill_customize = "NO"
            if weapon.isSkillCustomEnabled:
                skill_customize = "YES"

            stat_customize = "NO"
            if weapon.isParameterCustomEnabled:
                stat_customize = "YES"
            
            embed = Embed(title=weapon.name, type="rich", colour=color)
            embed.set_thumbnail(url=IMAGE_URL.format(weapon.resourceName))
            embed.add_field(name="Rarity", value=rarity, inline=True)
            embed.add_field(name="Cost", value=str(weapon.deckCost), inline=True)
            embed.add_field(name="Max Level", value=str(weapon.maxLevel), inline=True)
            embed.add_field(name="PAtk", value=str(weapon.maxAttack), inline=True)
            embed.add_field(name="PDef", value=str(weapon.maxDefence), inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="MAtk", value=str(weapon.maxMagicAttack), inline=True)
            embed.add_field(name="MDef", value=str(weapon.maxMagicDefence), inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="Story Skill", value=story_skill.name, inline=False)
            embed.add_field(name="Colosseum Skill", value=colo_skill.name, inline=True)
            embed.add_field(name="Colosseum Support Skill", value=colo_supp_skill.name, inline=True)

            embed.set_footer(text=f"Infinity Weapon: {infinity_weapon} | Skill Customizable: {skill_customize} | Stat Customizable: {stat_customize}")

            await ctx.channel.send(embed=embed)


if __name__ == "__main__":
    bot.run(token)
