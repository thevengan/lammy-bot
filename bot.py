# nextcord import
import nextcord
from nextcord import SelectOption
from nextcord.ext import commands, tasks

# default library imports
import os
import requests
import json
from datetime import time, datetime

# non-default imports
from sqlalchemy import or_

# local imports
from schedules import GUERRILLA_TIMES, CONQUEST_TIMES, PURIFICATION_TIMES
from models import Card, CardEvolution, Character, DiscordMessage, Skill, GuildToggle, GuildMessageChannel
from crud import recreate_database, populate_database, session_scope
from constants import BOT_CHANNELS, VERSION_URL, HELP_MESSAGE, HELP_MESSAGE_CONT
from embed_helper import JobHelper, NightmareHelper, SkillHelper, WeaponHelper
from helpers import integer_to_roman
from views import NightmareView, SkillDropdown, SkillView, WeaponView

# set the nextcord bot token
token = os.getenv("DISCORD_BOT_TOKEN")

description = "TODO: Change Me"

intents = nextcord.Intents.default()
intents.members = True

# instantiate bot
bot = commands.Bot(command_prefix='!', description=description, intents=intents)


# ping_role task that acts every minute and pings applicable roles
@tasks.loop(minutes=1)
async def ping_role():
    current_time = time(datetime.now().hour, datetime.now().minute)

    guilds = bot.guilds
    guilds_chunked = []
    while guilds:
        try:
            guilds_chunked.append(guilds[:30])
            del guilds[:30]
        except IndexError:
            guilds_chunked.append(guilds)
            del guilds[:]

    if current_time in GUERRILLA_TIMES:
        for chunk in guilds_chunked:
            for guild in chunk:
                with session_scope() as s:
                    db_entry = s.query(GuildToggle).filter(GuildToggle.guild_id==guild.id).first()
                    guild_db_entry = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==guild.id).first()

                    guild_channel_id = None
                    if guild_db_entry:
                        guild_channel_id = guild_db_entry.channel_id

                    if db_entry is None:
                        if guild_channel_id:
                            channels = [channel for channel in guild.channels if channel.id == guild_channel_id]
                        else:
                            channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                        try:
                            role = [role for role in guild.roles if role.name == "sino_guerrilla"][0]

                            for channel in channels:
                                await channel.send(f"{role.mention}: Guerrilla is open for the next 30 minutes!")
                        except IndexError:
                            continue
                    elif db_entry.guerrilla:
                        if guild_channel_id:
                            channels = [channel for channel in guild.channels if channel.id == guild_channel_id]
                        else:
                            channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                        try:
                            role = [role for role in guild.roles if role.name == "sino_guerrilla"][0]

                            for channel in channels:
                                await channel.send(f"{role.mention}: Guerrilla is open for the next 30 minutes!")
                        except IndexError:
                            continue
    
    if current_time in CONQUEST_TIMES:
        for chunk in guilds_chunked:
            for guild in chunk:
                with session_scope() as s:
                    db_entry = s.query(GuildToggle).filter(GuildToggle.guild_id==guild.id).first()
                    guild_db_entry = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==guild.id).first()

                    guild_channel_id = None
                    if guild_db_entry:
                        guild_channel_id = guild_db_entry.channel_id

                    if db_entry is None:
                        if guild_channel_id:
                            channels = [channel for channel in guild.channels if channel.id == guild_channel_id]
                        else:
                            channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                        try:
                            role = [role for role in guild.roles if role.name == "sino_conquest"][0]

                            for channel in channels:
                                await channel.send(f"{role.mention}: Conquest is open for the next 30 minutes!")
                        except IndexError:
                            continue
                    elif db_entry.conquest:
                        if guild_channel_id:
                            channels = [channel for channel in guild.channels if channel.id == guild_channel_id]
                        else:
                            channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                            try:
                                role = [role for role in guild.roles if role.name == "sino_conquest"][0]

                                for channel in channels:
                                    await channel.send(f"{role.mention}: Conquest is open for the next 30 minutes!")
                            except IndexError:
                                continue

    if current_time in PURIFICATION_TIMES:
        for chunk in guilds_chunked:
            for guild in chunk:
                with session_scope() as s:
                    db_entry = s.query(GuildToggle).filter(GuildToggle.guild_id==guild.id).first()
                    guild_db_entry = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==guild.id).first()

                    guild_channel_id = None
                    if guild_db_entry:
                        guild_channel_id = guild_db_entry.channel_id

                    if db_entry is None:
                        if guild_channel_id:
                            channels = [channel for channel in guild.channels if channel.id == guild_channel_id]
                        else:
                            channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                        try:
                            role = [role for role in guild.roles if role.name == "sino_purification"][0]

                            for channel in channels:
                                await channel.send(f"{role.mention}: Time to purify! Get that room clean!")
                        except IndexError:
                            continue
                    elif db_entry.purification:
                        if guild_channel_id:
                            channels = [channel for channel in guild.channels if channel.id == guild_channel_id]
                        else:
                            channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                            try:
                                role = [role for role in guild.roles if role.name == "sino_purification"][0]

                                for channel in channels:
                                    await channel.send(f"{role.mention}: Time to purify! Get that room clean!")
                            except IndexError:
                                continue    


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

    new_date = {'lastUpdatedTime': datamine_version}
    with open("version.json", "w") as f:
        json.dump(new_date, f)


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

    await bot.change_presence(activity=nextcord.Game(name="!soahelp"))


# help command - sends a help DM to the caller
@bot.command()
async def soahelp(ctx):
    await ctx.author.send(content=HELP_MESSAGE)
    await ctx.author.send(content=HELP_MESSAGE_CONT)


# initialize command - sets up necessary channels and roles
@bot.command()
async def soainitialize(ctx):
    channel_names = set([channel.name for channel in ctx.guild.channels])

    channel_intersection = channel_names & set(BOT_CHANNELS)

    channels_added = []
    if not channel_intersection:
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
        await ctx.channel.send(f"{ctx.author.mention}: usable channel(s) already exists - {channel_intersection}.")
    if roles_added:
        await ctx.channel.send(f"{ctx.author.mention}: Created the following roles - {roles_added}.")
    else:
        await ctx.channel.send(f"{ctx.author.mention}: Roles already exist.")


# giverole command - gives the specified role(s) to the caller
@bot.command()
async def soagiverole(ctx):
    with session_scope() as s:
        guild = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==ctx.guild.id).first()

        if guild:
            guild_channel_id = guild.channel_id

    if ctx.channel.name in BOT_CHANNELS or ctx.channel.id == guild_channel_id:
        roles_added = []
        roles_not_added = []

        if "guerrilla" in ctx.message.content:
            roles = [role for role in ctx.guild.roles if role.name == "sino_guerrilla"]
            user_roles = [role for role in ctx.author.roles]
            for role in roles:
                if role not in user_roles:
                    await ctx.author.add_roles(role)
                    roles_added.append("sino_guerrilla")
                else:
                    roles_not_added.append("sino_guerrilla")

        if "conquest" in ctx.message.content:
            roles = [role for role in ctx.guild.roles if role.name == "sino_conquest"]
            user_roles = [role for role in ctx.author.roles]
            for role in roles:
                if role not in user_roles:
                    await ctx.author.add_roles(role)
                    roles_added.append("sino_conquest")
                else:
                    roles_not_added.append("sino_conquest")

        if "purification" in ctx.message.content:
            roles = [role for role in ctx.guild.roles if role.name == "sino_purification"]
            user_roles = [role for role in ctx.author.roles]
            for role in roles:
                if role not in user_roles:
                    await ctx.author.add_roles(role)
                    roles_added.append("sino_purification")
                else:
                    roles_not_added.append("sino_purification")

        if roles_added:
            await ctx.channel.send(f"{ctx.author.mention}: You've been given the following role(s) - {roles_added}.")
        if roles_not_added:
            await ctx.channel.send(f"{ctx.author.mention}: You're already in the following role(s) - {roles_not_added}.")
        if not roles_added or roles_not_added:
            await ctx.channel.send(f"{ctx.author.mention}: Sorry, that's not a valid role.")


# removerole command - removes the specified role(s) from the caller
@bot.command()
async def soaremoverole(ctx):
    with session_scope() as s:
        guild = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==ctx.guild.id).first()

        if guild:
            guild_channel_id = guild.channel_id

    if ctx.channel.name in BOT_CHANNELS or ctx.channel.id == guild_channel_id:
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


# guildtoggle command - toggles whether the @mentions for conq, guerr, and puri are enabled
@bot.command()
async def soatoggle(ctx):
    with session_scope() as s:
        guild = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==ctx.guild.id).first()

        if guild:
            guild_channel_id = guild.channel_id

    if ctx.channel.name in BOT_CHANNELS or ctx.channel.id == guild_channel_id:
        actions_enabled = []
        actions_disabled = []

        with session_scope() as s:
            guild = s.query(GuildToggle).filter(GuildToggle.guild_id==ctx.guild.id).first()

            if guild:
                if "guerrilla" in ctx.message.content:
                    if guild.guerrilla:
                        guild.guerrilla = not guild.guerrilla
                        actions_disabled.append("Guerrilla")
                    else:
                        guild.guerrilla = not guild.guerrilla
                        actions_enabled.append("Guerrilla")
                if "conquest" in ctx.message.content:
                    if guild.conquest:
                        guild.conquest = not guild.conquest
                        actions_disabled.append("Conquest")
                    else:
                        guild.conquest = not guild.conquest
                        actions_enabled.append("Conquest")
                if "purification" in ctx.message.content:
                    if guild.purification:
                        guild.purification = not guild.purification
                        actions_disabled.append("Purification")
                    else:
                        guild.purification = not guild.purification
                        actions_enabled.append("Purification")
            else:
                new_guild = GuildToggle(
                    guild_id=ctx.guild.id
                )
                s.add(new_guild)
                guild = s.query(GuildToggle).filter(GuildToggle.guild_id==ctx.guild.id).first()

                if "guerrilla" in ctx.message.content:
                    if guild.guerrilla:
                        guild.guerrilla = not guild.guerrilla
                        actions_disabled.append("Guerrilla")
                    else:
                        guild.guerrilla = not guild.guerrilla
                        actions_enabled.append("Guerrilla")
                if "conquest" in ctx.message.content:
                    if guild.conquest:
                        guild.conquest = not guild.conquest
                        actions_disabled.append("conquest")
                    else:
                        guild.conquest = not guild.conquest
                        actions_enabled.append("conquest")
                if "purification" in ctx.message.content:
                    if guild.purification:
                        guild.purification = not guild.purification
                        actions_disabled.append("purification")
                    else:
                        guild.purification = not guild.purification
                        actions_enabled.append("purification")

        if actions_enabled:
            await ctx.channel.send(f"{ctx.author.mention}: The following @mention(s) have been TURNED ON - {actions_enabled}.")
        if actions_disabled:
            await ctx.channel.send(f"{ctx.author.mention}: The following @mention(s) have been TURNED OFF - {actions_disabled}.")


# channel command - sets a custom channel for lammy-bot to listen and respond to comamnds
@bot.command()
async def soachannel(ctx):
    with session_scope() as s:
        guild = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==ctx.guild.id).first()

        if guild:
            guild_channel_id = guild.channel_id

    if ctx.channel.name in BOT_CHANNELS or ctx.channel.id == guild_channel_id:
        channel_name = ctx.message.content[12:].strip()

        if "" == channel_name:
            return

        with session_scope() as s:
            guild = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==ctx.guild.id).first()

            if guild:
                try:
                    channel_id = [channel.id for channel in ctx.guild.channels if channel.name == channel_name][0]
                    if guild.channel_id == channel_id:
                        await ctx.channel.send(f"{ctx.author.mention}: that custom channel is already set.")
                    else:
                        guild.channel_id = channel_id
                        await ctx.channel.send(f"{ctx.author.mention}: '{ctx.guild.get_channel(channel_id).name}' has been set as the custom channel.")
                except IndexError:
                    await ctx.channel.send(f"{ctx.author.mention}: I couldn't find that channel in this server.")

            else:
                try:
                    channel_id = [channel.id for channel in ctx.guild.channels if channel.name == channel_name][0]
                    new_guild = GuildMessageChannel(
                        guild_id = ctx.guild.id,
                        channel_id = channel_id
                    )
                    s.add(new_guild)

                    await ctx.channel.send(f"{ctx.author.mention}: '{ctx.guild.get_channel(channel_id).name}' has been set as the custom channel.")
                except IndexError:
                    await ctx.channel.send(f"{ctx.author.mention}: I couldn't find that channel in this server.")


# weapon command - queries the db and displays information about the requested weapon
@bot.command()
async def soaweapon(ctx):
    with session_scope() as s:
        guild = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==ctx.guild.id).first()

        if guild:
            guild_channel_id = guild.channel_id

    if ctx.channel.name in BOT_CHANNELS or ctx.channel.id == guild_channel_id:
        weapon_name = ctx.message.content[11:].strip()

        if "" == weapon_name:
            return

        with session_scope() as s:
            weapon = s.query(Card).filter(Card.name.ilike(f"%{weapon_name.replace(' ', '%')}%"), Card.evolutionLevel==0, Card.cardType==1, Card.isRelease).first()

            if weapon is None:
                await ctx.channel.send(f"{ctx.author.mention}: I couldn't find a weapon matching {weapon_name}. Please try again.")
                return
            
            helper = WeaponHelper(weapon)
            embed = helper.create_embed()
            view = WeaponView()

            evolution = s.query(CardEvolution).filter(CardEvolution.cardMstId==weapon.cardMstId).first()

            response = await ctx.channel.send(embed=embed, view=view)
            message_meta_data = DiscordMessage(
                message_id=response.id,
                last_updated=datetime.now(),
                prev=None,
                curr=weapon.cardMstId,
                next=evolution.evolvedCardMstId if evolution else None
            )
            s.add(message_meta_data)


# skill command - queries the db and displays information about the requested skill
@bot.command()
async def soaskill(ctx):
    with session_scope() as s:
        guild = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==ctx.guild.id).first()

        if guild:
            guild_channel_id = guild.channel_id

    if ctx.channel.name in BOT_CHANNELS or ctx.channel.id == guild_channel_id:
        skill_name = ctx.message.content[10:].strip()

        if "" == skill_name:
            return

        for section in skill_name.split():
            if section.isdecimal():
                new_section = integer_to_roman(int(section))
                skill_name = skill_name.replace(section, new_section)

        with session_scope() as s:
            skill = s.query(Skill).filter(Skill.name.ilike(f"%{skill_name.replace(' ', '%')}%"), Skill.category != 4).first()

            if skill is None:
                await ctx.channel.send(f"{ctx.author.mention}: I couldn't find a skill matching {skill_name}. Please try again.")
                return

            helper = SkillHelper(skill)
            embed = helper.create_embed()

            skill_alts = s.query(Skill).filter(Skill.name==skill.name, Skill.category != 4).all()
            alt_costs = [SelectOption(label=f"{skill.sp} (ID: {skill.skillMstId})") for skill in skill_alts]
            dropdown = SkillDropdown(alt_costs)
            view = SkillView(dropdown)

            await ctx.channel.send(embed=embed, view=view)


# nightmare command - queries the db and displays information about the requested nightmare
@bot.command()
async def soanightmare(ctx):
    with session_scope() as s:
        guild = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==ctx.guild.id).first()

        if guild:
            guild_channel_id = guild.channel_id

    if ctx.channel.name in BOT_CHANNELS or ctx.channel.id == guild_channel_id:
        nightmare_name = ctx.message.content[14:].strip()

        if "" == nightmare_name:
            return

        with session_scope() as s:
            nightmare = s.query(Card).filter(Card.name.ilike(f"%{nightmare_name.replace(' ', '%')}%"), Card.cardType==3, Card.isRelease).first()

            if nightmare is None:
                await ctx.channel.send(f"{ctx.author.mention}: I couldn't find a nightmare matching {nightmare_name}. Please try again.")
                return
            
            helper = NightmareHelper(nightmare)
            embed = helper.create_embed()
            view = NightmareView()

            evolution = s.query(CardEvolution).filter(CardEvolution.cardMstId==nightmare.cardMstId).first()

            response = await ctx.channel.send(embed=embed, view=view)
            message_meta_data = DiscordMessage(
                message_id=response.id,
                last_updated=datetime.now(),
                prev=None,
                curr=nightmare.cardMstId,
                next=evolution.evolvedCardMstId if evolution else None
            )
            s.add(message_meta_data)


# job command - queries the db and displays information about the requested job
@bot.command()
async def soajob(ctx):
    with session_scope() as s:
        guild = s.query(GuildMessageChannel).filter(GuildMessageChannel.guild_id==ctx.guild.id).first()

        if guild:
            guild_channel_id = guild.channel_id

    if ctx.channel.name in BOT_CHANNELS or ctx.channel.id == guild_channel_id:
        entry = ctx.message.content[8:].strip()

        if "" == entry:
            return

        character_name = entry.split('/')[0]
        class_name = entry.split('/')[1]

        with session_scope() as s:
            character = s.query(Character).filter(
                Character.characterUniqueName.ilike(f"%{character_name}%"), 
                Character.name.ilike(f"%{class_name}%"), 
                or_(
                    Character.displayStartTime!=1924959599, 
                    Character.displayStartTime.is_(None))
                    ).first()

            if character is None:
                await ctx.channel.send(f"{ctx.author.mention}: I couldn't find a job matching {character_name}/{class_name}. Please try again.")
                return

            helper = JobHelper(character)
            embed = helper.create_embed()

            await ctx.channel.send(embed=embed)


if __name__ == "__main__":
    bot.run(token)
