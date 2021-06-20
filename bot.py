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
from sqlalchemy import and_, or_

# local imports
from schedules import GUERRILLA_TIMES, CONQUEST_TIMES, PURIFICATION_TIMES
from models import Card, CardEvolution, Item, Skill, LimitBreakSkill, Character, CharacterAbility
from crud import recreate_database, populate_database, session_scope
from constants import BOT_CHANNELS, IMAGE_URL, VERSION_URL, WEAPON_ICON_URL, \
    BUFF_SKILL_PRIMARY_ICON_VALUES, DEBUFF_SKILL_PRIMARY_ICON_VALUES

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
        print("recreating db")
        recreate_database()
        populate_database()

    # TODO: write to version.json so we don't always update the DB with a deploy

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

# help command - sends a help DM to the caller
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

        if "" == weapon_name.strip():
            return

        with session_scope() as s:
            weapon = s.query(Card).filter(and_(Card.name.ilike(f'%{weapon_name}%'), Card.evolutionLevel==0, Card.cardType==1)).first()

            if weapon is None:
                await ctx.channel.send(f"{ctx.author.mention}: I couldn't find a weapon matching {weapon_name}. Please try again.")
                return

            story_skill = s.query(Skill).filter(Skill.skillMstId==weapon.questSkillMstId).first()
            colo_skill = s.query(Skill).filter(Skill.skillMstId==weapon.frontSkillMstId).first()
            colo_supp_skill = s.query(Skill).filter(Skill.skillMstId==weapon.autoSkillMstId).first()

            color = 0x000000
            if weapon.attribute == 1:
                color = 0xDA230E
            if weapon.attribute == 2:
                color = 0x080B72
            if weapon.attribute == 3:
                color = 0x1F7310

            rarity = "A"
            if weapon.rarity == 4:
                rarity = "S"
            if weapon.rarity == 5:
                rarity = "SR"
            if weapon.rarity == 6:
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

@bot.command()
async def soaskill(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        skill_name = ctx.message.content[10:]

        if "" == skill_name.strip():
            return

        with session_scope() as s:
            skill = s.query(Skill).filter(and_(Skill.name.ilike(f"%{skill_name}%"), Skill.category != 4)).first()

            if skill is None:
                await ctx.channel.send(f"{ctx.author.mention}: I couldn't find a skill matching {skill_name}. Please try again.")
                return

            description = skill.description.replace("\\n", " ")
            description = description + "\n\nWeapons with skill: "
            weapons_with_skill = list(set([
                weapon.name for weapon in s.query(Card).filter(or_(
                Card.questSkillMstId==skill.skillMstId, 
                Card.frontSkillMstId==skill.skillMstId, 
                Card.autoSkillMstId==skill.skillMstId)).limit(20).all()
                ]))
            for weapon in weapons_with_skill:
                description = description + weapon + ", "
            description = description[:-2] + "."

            color = 0x000000
            if skill.primaryIcon == 1:
                color = 0x8B0000
            if skill.primaryIcon == 2:
                color = 0x00008B
            if skill.primaryIcon == 3:
                color = 0xFFFFFF
            if skill.primaryIcon in BUFF_SKILL_PRIMARY_ICON_VALUES:
                color = 0x6A0DAD
            if skill.primaryIcon in DEBUFF_SKILL_PRIMARY_ICON_VALUES:
                color = 0x006D5B

            weapon_icon = ""
            if skill.primaryIcon == 1 and skill.rangeIcon == 1:
                weapon_icon = "1aBXxZdj0QvOEhrfdD5A0Vn7wUGPwpkGa"
            if skill.primaryIcon == 1 and skill.rangeIcon > 1:
                weapon_icon = "1amsazOzjdKAjELxTVbD92imxgtMgpxYv"
            if skill.primaryIcon == 2 and skill.rangeIcon == 1:
                weapon_icon = "15o-B24K2YeGXmPIUE6cTBXc7xkSfVDpm"
            if skill.primaryIcon == 2 and skill.rangeIcon > 1:
                weapon_icon = "1X3fdAZUMtKsXxjNbv1J5C_05Sj42QbN4"
            if skill.primaryIcon in BUFF_SKILL_PRIMARY_ICON_VALUES:
                weapon_icon = "1N_BYaXFrBjKzPEIFex2ywsWDPbnxcahz"
            if skill.primaryIcon in DEBUFF_SKILL_PRIMARY_ICON_VALUES:
                weapon_icon = "11rm0tpaxFYoInn6m0KguU8ND9zmlLZUF"
            if skill.primaryIcon == 3:
                weapon_icon = "1ALhoczKu4VyQTzeEscTGVCOG0E0V3Mp9"

            embed = Embed(title=skill.name, description=description, type="rich", colour=color)
            embed.set_thumbnail(url=WEAPON_ICON_URL.format(weapon_icon))
            embed.add_field(name="SP", value=str(skill.sp), inline=True)
            embed.add_field(name="Targets", value=f"{skill.typeLabel if skill.typeLabel != 'own' else 'Self'}", inline=True)

            await ctx.channel.send(embed=embed)


if __name__ == "__main__":
    bot.run(token)
