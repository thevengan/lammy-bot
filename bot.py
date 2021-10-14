# discord import
import discord
from discord import Embed
from discord import channel
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
from models import Card, CardEvolution, Skill, DiscordMessage
from crud import recreate_database, populate_database, session_scope
from constants import BOT_CHANNELS, VERSION_URL, WEAPON_ICON_URL, \
    BUFF_SKILL_PRIMARY_ICON_VALUES, DEBUFF_SKILL_PRIMARY_ICON_VALUES
from embed_helper import WeaponHelper, NightmareHelper

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
            channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
            role = [role for role in guild.roles if role.name == "sino_guerrilla"][0]

            for channel in channels:
                await channel.send(f"{role.mention}: Guerrilla is open for the next 30 minutes!")
    
    if current_time in CONQUEST_TIMES:
        for guild in bot.guilds:
            channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
            role = [role for role in guild.roles if role.name == "sino_conquest"][0]

            for channel in channels:
                await channel.send(f"{role.mention}: Conquest is open for the next 30 minutes!")

    if current_time in PURIFICATION_TIMES:
        for guild in bot.guilds:
            channels = [channel for channel in guild.channels if channel.name in BOT_CHANNELS]
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
        message = """**Available Commands**
**Prefix** - use `!soa[command]` to access bot commands - eg. `!soahelp`
- `help` : sends a DM to the message author detailing the commands available.

- `initialize` : creates the necessary channels and roles for `lammy-bot` to function.
      - what this entails - creates `sino_conquest`, `sino_guerrilla`, and `sino_purification` as server roles. Creates the `bot-spam` channel for using other commands.

- `giverole [role]` : gives the message author the requested role(s). Multiple roles can be given by separating them with a `space`. Possible roles are `conquest, guerrilla, purification`.
      - example - `!soagiverole conquest guerrilla` would give the message author the `sino_conquest` and `sino_guerrilla` roles.

- `removerole [role]` : removes the requested role(s) from the message author. Multiple roles can be given by separating them with a `space`. Possible roles are `conquest, guerrilla, purification`.
      - example - `!soaremoverole purification` would remove the `sino_purification` role from the message author.

- `weapon [weapon]`: searches the weapon database for the text entered after the command and returns an embed with information on the most relevant weapon.
      - example - `!soaweapon entrail` would pull up an embed with information for `Entrails of Justice`.

- `skill [skill]` : searches the skill database for the text entered after the command and returns an embed with information on the most relevant skill.
      - example - `!soaskill hero's harmony` would pull up an embed with information for `Hero's Harmony (I)`.

- `nightmare [nightmare]` : searches the nightmare database for the text entered after the command and returns an embed with information on the most relevant nightmare.
      - example `!soanightmare uga` would pull up an embed with information for `Ugallu`.
      
**lammy-bot will ONLY work in the following channels - `bot-spam`, `spam-bot`, `bot-commands`, `bot-only`, `bots-only`"""
        await ctx.author.send(content=message)

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

# weapon command - queries the db and displays information about the requested weapon
@bot.command()
async def soaweapon(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        weapon_name = ctx.message.content[11:].strip()

        if "" == weapon_name.strip():
            return

        with session_scope() as s:
            weapon = s.query(Card).filter(and_(Card.name.ilike(f'%{weapon_name}%'), Card.evolutionLevel==0, Card.cardType==1)).first()

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


# nightmare command - queries the db and displays information about the requested nightmare
@bot.command()
async def soanightmare(ctx):
    if ctx.channel.name in BOT_CHANNELS:
        nightmare_name = ctx.message.content[14:].strip()

        if "" == nightmare_name.strip():
            return

        with session_scope() as s:
            nightmare = s.query(Card).filter(and_(Card.name.ilike(f"%{nightmare_name}%"), Card.cardType==3)).first()

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
