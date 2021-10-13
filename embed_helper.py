from discord import Embed

from constants import IMAGE_URL
from crud import session_scope
from models import Card, CardEvolution, Skill

class WeaponHelper:
    def __init__(self, weapon):
        self.weapon = weapon

    def create_embed(self):
        with session_scope() as s:
            weapon = self.weapon

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

            return embed


class NightmareHelper:
    def __init__(self, nightmare):
        self.nightmare = nightmare

    def create_embed(self):
        with session_scope() as s:
            nightmare = self.nightmare

            rarity = "A"
            if nightmare.rarity == 4:
                rarity = "S"
            if nightmare.rarity == 5:
                rarity = "SR"
            if nightmare.rarity == 6:
                rarity = "L"

            embed = Embed(title=nightmare.name, type="rich", colour=0xFFFFFF)
            embed.set_thumbnail(url=IMAGE_URL.format(nightmare.resourceName))
            embed.add_field(name="Rarity", value=rarity, inline=True)
            embed.add_field(name="Max Level", value=str(nightmare.maxLevel), inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="PAtk", value=str(nightmare.maxAttack), inline=True)
            embed.add_field(name="PDef", value=str(nightmare.maxDefence), inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="MAtk", value=str(nightmare.maxMagicAttack), inline=True)
            embed.add_field(name="MDef", value=str(nightmare.maxMagicDefence), inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)

            return embed