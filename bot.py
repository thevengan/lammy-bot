# discord import
import discord
from discord import Embed
from discord.ext import commands, tasks

# default library imports
import os
import requests
import json
from datetime import time, datetime
from time import sleep

# non default imports
from sqlalchemy import and_, or_

# local imports
from schedules import GUERRILLA_TIMES, CONQUEST_TIMES, PURIFICATION_TIMES
from models import Card, CardEvolution, Character, DiscordMessage, Skill, GuildToggle
from crud import recreate_database, populate_database, session_scope
from constants import BOT_CHANNELS, VERSION_URL, WEAPON_ICON_URL, \
    BUFF_SKILL_PRIMARY_ICON_VALUES, DEBUFF_SKILL_PRIMARY_ICON_VALUES, HELP_MESSAGE, HELP_MESSAGE_CONT
from embed_helper import JobHelper, NightmareHelper, WeaponHelper
from helpers import integer_to_roman

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
            with session_scope() as s:
                db_entry = s.query(GuildToggle).filter(GuildToggle.guild_id==guild.id).first()

                if db_entry is None:
                    channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                    try:
                        role = [role for role in guild.roles if role.name == "sino_guerrilla"][0]

                        for channel in channels:
                            await channel.send(f"{role.mention}: Guerrilla is open for the next 30 minutes!")
                    except IndexError:
                        continue
                else:
                    if db_entry.guerrilla:
                        channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                        try:
                            role = [role for role in guild.roles if role.name == "sino_guerrilla"][0]

                            for channel in channels:
                                await channel.send(f"{role.mention}: Guerrilla is open for the next 30 minutes!")
                        except IndexError:
                            continue
    
    if current_time in CONQUEST_TIMES:
        for guild in bot.guilds:
            with session_scope() as s:
                db_entry = s.query(GuildToggle).filter(GuildToggle.guild_id==guild.id).first()

                if db_entry is None:
                    channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                    try:
                        role = [role for role in guild.roles if role.name == "sino_conquest"][0]

                        for channel in channels:
                            await channel.send(f"{role.mention}: Conquest is open for the next 30 minutes!")
                    except IndexError:
                        continue
                else:
                    if db_entry.conquest:
                        channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                        try:
                            role = [role for role in guild.roles if role.name == "sino_conquest"][0]

                            for channel in channels:
                                await channel.send(f"{role.mention}: Conquest is open for the next 30 minutes!")
                        except IndexError:
                            continue

    if current_time in PURIFICATION_TIMES:
        for guild in bot.guilds:
            with session_scope() as s:
                db_entry = s.query(GuildToggle).filter(GuildToggle.guild_id==guild.id).first()

                if db_entry is None:
                    channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
                    try:
                        role = [role for role in guild.roles if role.name == "sino_purification"][0]

                        for channel in channels:
                            await channel.send(f"{role.mention}: Time to purify! Get that room clean!")
                    except IndexError:
                        continue
                else:
                    if db_entry.purification:
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

    await bot.change_presence(activity=discord.Game(name="!soahelp"))


# help command - sends a help DM to the caller
@bot.command()
async def soahelp(ctx):
    if ctx.channel.name in BOT_CHANNELS:
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


# guildtoggle command - toggles whether the @mentions for conq, guerr, and puri are enabled
@bot.command()
async def soatoggle(ctx):
    if ctx.channel.name in BOT_CHANNELS:
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


# weapon command - queries the db and displays information about the requested weapon
@bot.command()
async def soaweapon(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        weapon_name = ctx.message.content[11:].strip()

        if "" == weapon_name:
            return

        with session_scope() as s:
            weapon = s.query(Card).filter(and_(Card.name.ilike(f"%{weapon_name.replace(' ', '%')}%"), Card.evolutionLevel==0, Card.cardType==1)).first()

            if weapon is None:
                await ctx.channel.send(f"{ctx.author.mention}: I couldn't find a weapon matching {weapon_name}. Please try again.")
                return
            
            helper = WeaponHelper(weapon)
            embed = helper.create_embed()

            evolution = s.query(CardEvolution).filter(CardEvolution.cardMstId==weapon.cardMstId).first()

            response = await ctx.channel.send(embed=embed)
            message_meta_data = DiscordMessage(
                message_id=response.id,
                last_updated=datetime.now(),
                card_type="weapon",
                prev=None,
                curr=weapon.cardMstId,
                next=evolution.evolvedCardMstId if evolution else None
            )
            s.add(message_meta_data)

            evolve_emoji = ctx.bot.get_emoji(897679174712578109)
            await response.add_reaction(evolve_emoji)


# skill command - queries the db and displays information about the requested skill
@bot.command()
async def soaskill(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        skill_name = ctx.message.content[10:].strip()

        if "" == skill_name:
            return

        for section in skill_name.split():
            if section.isdecimal():
                new_section = integer_to_roman(int(section))
                skill_name = skill_name.replace(section, new_section)

        with session_scope() as s:
            skill = s.query(Skill).filter(and_(Skill.name.ilike(f"%{skill_name.replace(' ', '%')}%"), Skill.category != 4)).first()

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


# nightmare command - queries the db and displays information about the requested nightmare
@bot.command()
async def soanightmare(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        nightmare_name = ctx.message.content[14:].strip()

        if "" == nightmare_name:
            return

        with session_scope() as s:
            nightmare = s.query(Card).filter(and_(Card.name.ilike(f"%{nightmare_name.replace(' ', '%')}%"), Card.cardType==3)).first()

            if nightmare is None:
                await ctx.channel.send(f"{ctx.author.mention}: I couldn't find a nightmare matching {nightmare_name}. Please try again.")
                return

            helper = NightmareHelper(nightmare)
            embed = helper.create_embed()

            evolution = s.query(CardEvolution).filter(CardEvolution.cardMstId==nightmare.cardMstId).first()

            response = await ctx.channel.send(embed=embed)
            message_meta_data = DiscordMessage(
                message_id=response.id,
                last_updated=datetime.now(),
                card_type="nightmare",
                prev=None,
                curr=nightmare.cardMstId,
                next=evolution.evolvedCardMstId if evolution else None
            )
            s.add(message_meta_data)

            evolve_emoji = ctx.bot.get_emoji(897679174712578109)
            await response.add_reaction(evolve_emoji)


# class command - queries the db and displays information about the requested class
@bot.command()
async def soaclass(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        entry = ctx.message.content[10:].strip()

        if "" == entry:
            return

        character_name = entry.split('/')[0]
        class_name = entry.split('/')[1]

        with session_scope() as s:
            character = s.query(Character).filter(and_(Character.characterUniqueName.ilike(f"%{character_name}%")), Character.name.ilike(f"%{class_name}%")).first()

            if character is None:
                await ctx.channel.send(f"{ctx.author.mention}: I couldn't find a class matching {character_name}/{class_name}. Please try again.")

            helper = JobHelper(character)
            embed = helper.create_embed()

            await ctx.channel.send(embed=embed)


# on_reaction_add event - used for evolving/devolving weapon and nightmare embeds
@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    if reaction.message.channel.name in BOT_CHANNELS:
        with session_scope() as s:
            evolve_emoji = bot.get_emoji(897679174712578109)
            devolve_emoji = bot.get_emoji(897679128671715369)
            message_id = reaction.message.id

            message_meta_data = s.query(DiscordMessage).filter(DiscordMessage.message_id==message_id).first()

            # evolve
            if reaction.emoji.id == evolve_emoji.id:
                next = message_meta_data.next
                # weapon
                if message_meta_data.card_type == "weapon":
                    await reaction.message.clear_reactions()
                    weapon = s.query(Card).filter(Card.cardMstId==next).first()
                    helper = WeaponHelper(weapon)
                    embed = helper.create_embed()

                    await reaction.message.edit(embed=embed)

                    evolution = s.query(CardEvolution).filter(CardEvolution.cardMstId==next).first()
                    
                    message_meta_data.last_updated = datetime.now()
                    message_meta_data.prev = message_meta_data.curr
                    message_meta_data.curr = message_meta_data.next
                    message_meta_data.next = evolution.evolvedCardMstId if evolution else None
                    
                    await reaction.message.add_reaction(devolve_emoji)
                    if evolution:
                        await reaction.message.add_reaction(evolve_emoji)

                # nightmare
                if message_meta_data.card_type == "nightmare":
                    await reaction.message.clear_reactions()
                    nightmare = s.query(Card).filter(Card.cardMstId==next).first()
                    helper = NightmareHelper(nightmare)
                    embed = helper.create_embed()

                    await reaction.message.edit(embed=embed)

                    evolution = s.query(CardEvolution).filter(CardEvolution.cardMstId==next).first()
                    
                    message_meta_data.last_updated = datetime.now()
                    message_meta_data.prev = message_meta_data.curr
                    message_meta_data.curr = message_meta_data.next
                    message_meta_data.next = evolution.evolvedCardMstId if evolution else None
                    
                    await reaction.message.add_reaction(devolve_emoji)
                    if evolution:
                        await reaction.message.add_reaction(evolve_emoji)

            # devolve
            if reaction.emoji.id == devolve_emoji.id:
                prev = message_meta_data.prev
                # weapon
                if message_meta_data.card_type == "weapon":
                    await reaction.message.clear_reactions()
                    weapon = s.query(Card).filter(Card.cardMstId==prev).first()
                    helper = WeaponHelper(weapon)
                    embed = helper.create_embed()

                    await reaction.message.edit(embed=embed)

                    devolution = s.query(CardEvolution).filter(CardEvolution.evolvedCardMstId==prev).first()

                    message_meta_data.last_updated = datetime.now()
                    message_meta_data.next = message_meta_data.curr
                    message_meta_data.curr = message_meta_data.prev
                    message_meta_data.prev = devolution.cardMstId if devolution else None

                    if devolution:
                        await reaction.message.add_reaction(devolve_emoji)
                    sleep(0.5)
                    await reaction.message.add_reaction(evolve_emoji)

                # nightmare
                if message_meta_data.card_type == "nightmare":
                    await reaction.message.clear_reactions()
                    nightmare = s.query(Card).filter(Card.cardMstId==prev).first()
                    helper = NightmareHelper(nightmare)
                    embed = helper.create_embed()

                    await reaction.message.edit(embed=embed)

                    devolution = s.query(CardEvolution).filter(CardEvolution.evolvedCardMstId==prev).first()

                    message_meta_data.last_updated = datetime.now()
                    message_meta_data.next = message_meta_data.curr
                    message_meta_data.curr = message_meta_data.prev
                    message_meta_data.prev = devolution.cardMstId if devolution else None

                    if devolution:
                        await reaction.message.add_reaction(devolve_emoji)
                    sleep(0.5)
                    await reaction.message.add_reaction(evolve_emoji)
                

if __name__ == "__main__":
    bot.run(token)
