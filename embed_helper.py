from nextcord import Embed, colour
from sqlalchemy import or_
from sqlalchemy.sql.expression import desc
from tabulate import tabulate

from constants import IMAGE_URL, CLASS_IMAGE_URL, WEAPON_INTEGER_VALUES, \
    BUFF_SKILL_PRIMARY_ICON_VALUES, DEBUFF_SKILL_PRIMARY_ICON_VALUES, WEAPON_ICON_URL
from crud import session_scope
from models import Card, CharacterAbility, Skill

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


class JobHelper:
    def __init__(self, job):
        self.job = job

    def create_embed(self):
        with session_scope() as s:
            job = self.job

            job_levels = s.query(CharacterAbility).filter(CharacterAbility.characterMstId==job.characterMstId).all()

            if job.characterUniqueName == "Alice":
                color = 0x0076D4
            elif job.characterUniqueName == "Snow White":
                color = 0xFFFFFF
            elif job.characterUniqueName == "Red Riding Hood":
                color = 0x950400
            elif job.characterUniqueName == "Cinderella":
                color = 0xCCAAB2
            elif job.characterUniqueName == "Pinocchio":
                color = 0xD4F129
            elif job.characterUniqueName == "Sleeping Beauty":
                color = 0xEEDE90
            elif job.characterUniqueName == "Gretel":
                color = 0xF82DBF
            elif job.characterUniqueName == "Princess Kaguya":
                color = 0xC79DF6
            elif job.characterUniqueName == "Dorothy":
                color = 0x6A3755
            elif job.characterUniqueName == "Little Mermaid":
                color = 0x78E2EC
            elif job.characterUniqueName == "The Three Little Pigs":
                color = 0xA2928E
            elif job.characterUniqueName == "Aladdin":
                color = 0xC4A688
            elif job.characterUniqueName == "Rapunzel":
                color = 0xD97F2F
            elif job.characterUniqueName == "Hamelin":
                color = 0x4940C7
            elif job.characterUniqueName == "Nutcracker":
                color = 0xFDF4BF
            else:
                color = 0x525252

            level_text = ""
            for level in job_levels:
                if level.skillType == 1:
                    level_text = level_text + f"{level.releaseLevel}: (Common) {level.name}\n"
                elif level.skillType == 2:
                    level_text = level_text + f"{level.releaseLevel}: (Class) {level.name}\n"
                elif level.skillType == 3 or level.skillType == 4:
                    level_text = level_text + f"{level.releaseLevel}: (Support) {level.name}\n"

            weapon_affinity_dict = {}
            weapon_affinity_dict[" "] = [WEAPON_INTEGER_VALUES[job.favoriteWeapon]]

            for level in job_levels:
                if level.effectType == 6:
                    if "Fire" in level.name:
                        if level.cardDetailType == 0:
                            if "All (Fire)" not in weapon_affinity_dict[" "]:
                                weapon_affinity_dict[" "] = weapon_affinity_dict[" "] + ["All (Fire)"]

                            element_index = weapon_affinity_dict[" "].index("All (Fire)")
                            
                            if "+Area" in weapon_affinity_dict:
                                if len(weapon_affinity_dict["+Area"]) > 1:
                                    if len(weapon_affinity_dict["+Area"]) < element_index + 1:
                                        weapon_affinity_dict["+Area"] = weapon_affinity_dict["+Area"] + [level.effectValue]
                                    else:
                                        weapon_affinity_dict["+Area"][element_index] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = weapon_affinity_dict["+Area"] + [level.effectValue]
                            else:
                                weapon_affinity_dict["+Area"] = [0, level.effectValue]

                            if "Story" in weapon_affinity_dict:
                                if len(weapon_affinity_dict["Story"]) > 1:
                                    if len(weapon_affinity_dict["Story"]) < element_index + 1:
                                        weapon_affinity_dict["Story"] = weapon_affinity_dict["Story"] + [level.effectValue]
                                    else:
                                        weapon_affinity_dict["Story"][element_index] += level.effectValue
                                else:
                                    weapon_affinity_dict["Story"] = weapon_affinity_dict["Story"] + [level.effectValue]
                            else:
                                weapon_affinity_dict["Story"] = [0, level.effectValue]

                            if "Colo" in weapon_affinity_dict:
                                if len(weapon_affinity_dict["Colo"]) > 1:
                                    if len(weapon_affinity_dict["Colo"]) < element_index + 1:
                                        weapon_affinity_dict["Colo"] = weapon_affinity_dict["Colo"] + [level.effectValue]
                                    else:
                                        weapon_affinity_dict["Colo"][element_index] += level.effectValue
                                else:
                                    weapon_affinity_dict["Colo"] = weapon_affinity_dict["Colo"] + [level.effectValue]
                            else:
                                weapon_affinity_dict["Colo"] = [0, level.effectValue]
                        else:
                            if "Fire" not in weapon_affinity_dict[" "][0]:
                                weapon_affinity_dict[" "][0] += " (Fire)"

                            if "stage" in level.name:
                                if "+Area" in weapon_affinity_dict:
                                    weapon_affinity_dict["+Area"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = [level.effectValue]
                            elif "Story" in level.name:
                                if "+Area" in weapon_affinity_dict:
                                    weapon_affinity_dict["+Area"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = [level.effectValue]
                                if "Story" in weapon_affinity_dict:
                                    weapon_affinity_dict["Story"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Story"] = [level.effectValue]
                            else:
                                if "+Area" in weapon_affinity_dict:
                                    weapon_affinity_dict["+Area"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = [level.effectValue]
                                if "Story" in weapon_affinity_dict:
                                    weapon_affinity_dict["Story"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Story"] = [level.effectValue]
                                if "Colo" in weapon_affinity_dict:
                                    weapon_affinity_dict["Colo"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Colo"] = [level.effectValue]
                    elif "Water" in level.name:
                        if level.cardDetailType == 0:
                            if "All (Water)" not in weapon_affinity_dict[" "]:
                                weapon_affinity_dict[" "] = weapon_affinity_dict[" "] + ["All (Water)"]

                            element_index = weapon_affinity_dict[" "].index("All (Water)")
                            
                            if "+Area" in weapon_affinity_dict:
                                if len(weapon_affinity_dict["+Area"]) > 1:
                                    if len(weapon_affinity_dict["+Area"]) < element_index + 1:
                                        weapon_affinity_dict["+Area"] = weapon_affinity_dict["+Area"] + [level.effectValue]
                                    else:
                                        weapon_affinity_dict["+Area"][element_index] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = weapon_affinity_dict["+Area"] + [level.effectValue]
                            else:
                                weapon_affinity_dict["+Area"] = [0, level.effectValue]

                            if "Story" in weapon_affinity_dict:
                                if len(weapon_affinity_dict["Story"]) > 1:
                                    if len(weapon_affinity_dict["Story"]) < element_index + 1:
                                        weapon_affinity_dict["Story"] = weapon_affinity_dict["Story"] + [level.effectValue]
                                    else:
                                        weapon_affinity_dict["Story"][element_index] += level.effectValue
                                else:
                                    weapon_affinity_dict["Story"] = weapon_affinity_dict["Story"] + [level.effectValue]
                            else:
                                weapon_affinity_dict["Story"] = [0, level.effectValue]

                            if "Colo" in weapon_affinity_dict:
                                if len(weapon_affinity_dict["Colo"]) > 1:
                                    if len(weapon_affinity_dict["Colo"]) < element_index + 1:
                                        weapon_affinity_dict["Colo"] = weapon_affinity_dict["Colo"] + [level.effectValue]
                                    else:
                                        weapon_affinity_dict["Colo"][element_index] += level.effectValue
                                else:
                                    weapon_affinity_dict["Colo"] = weapon_affinity_dict["Colo"] + [level.effectValue]
                            else:
                                weapon_affinity_dict["Colo"] = [0, level.effectValue]
                        else:
                            if "Water" not in weapon_affinity_dict[" "][0]:
                                weapon_affinity_dict[" "][0] += " (Water)"

                            if "stage" in level.name:
                                if "+Area" in weapon_affinity_dict:
                                    weapon_affinity_dict["+Area"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = [level.effectValue]
                            elif "Story" in level.name:
                                if "+Area" in weapon_affinity_dict:
                                    weapon_affinity_dict["+Area"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = [level.effectValue]
                                if "Story" in weapon_affinity_dict:
                                    weapon_affinity_dict["Story"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Story"] = [level.effectValue]
                            else:
                                if "+Area" in weapon_affinity_dict:
                                    weapon_affinity_dict["+Area"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = [level.effectValue]
                                if "Story" in weapon_affinity_dict:
                                    weapon_affinity_dict["Story"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Story"] = [level.effectValue]
                                if "Colo" in weapon_affinity_dict:
                                    weapon_affinity_dict["Colo"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Colo"] = [level.effectValue]
                    elif "Wind" in level.name:
                        if level.cardDetailType == 0:
                            if "All (Wind)" not in weapon_affinity_dict[" "]:
                                weapon_affinity_dict[" "] = weapon_affinity_dict[" "] + ["All (Wind)"]

                            element_index = weapon_affinity_dict[" "].index("All (Wind)")
                            
                            if "+Area" in weapon_affinity_dict:
                                if len(weapon_affinity_dict["+Area"]) > 1:
                                    if len(weapon_affinity_dict["+Area"]) < element_index + 1:
                                        weapon_affinity_dict["+Area"] = weapon_affinity_dict["+Area"] + [level.effectValue]
                                    else:
                                        weapon_affinity_dict["+Area"][element_index] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = weapon_affinity_dict["+Area"] + [level.effectValue]
                            else:
                                weapon_affinity_dict["+Area"] = [0, level.effectValue]

                            if "Story" in weapon_affinity_dict:
                                if len(weapon_affinity_dict["Story"]) > 1:
                                    if len(weapon_affinity_dict["Story"]) < element_index + 1:
                                        weapon_affinity_dict["Story"] = weapon_affinity_dict["Story"] + [level.effectValue]
                                    else:
                                        weapon_affinity_dict["Story"][element_index] += level.effectValue
                                else:
                                    weapon_affinity_dict["Story"] = weapon_affinity_dict["Story"] + [level.effectValue]
                            else:
                                weapon_affinity_dict["Story"] = [0, level.effectValue]

                            if "Colo" in weapon_affinity_dict:
                                if len(weapon_affinity_dict["Colo"]) > 1:
                                    if len(weapon_affinity_dict["Colo"]) < element_index + 1:
                                        weapon_affinity_dict["Colo"] = weapon_affinity_dict["Colo"] + [level.effectValue]
                                    else:
                                        weapon_affinity_dict["Colo"][element_index] += level.effectValue
                                else:
                                    weapon_affinity_dict["Colo"] = weapon_affinity_dict["Colo"] + [level.effectValue]
                            else:
                                weapon_affinity_dict["Colo"] = [0, level.effectValue]
                        else:
                            if "Wind" not in weapon_affinity_dict[" "][0]:
                                weapon_affinity_dict[" "][0] += " (Wind)"

                            if "stage" in level.name:
                                if "+Area" in weapon_affinity_dict:
                                    weapon_affinity_dict["+Area"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = [level.effectValue]
                            elif "Story" in level.name:
                                if "+Area" in weapon_affinity_dict:
                                    weapon_affinity_dict["+Area"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = [level.effectValue]
                                if "Story" in weapon_affinity_dict:
                                    weapon_affinity_dict["Story"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Story"] = [level.effectValue]
                            else:
                                if "+Area" in weapon_affinity_dict:
                                    weapon_affinity_dict["+Area"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = [level.effectValue]
                                if "Story" in weapon_affinity_dict:
                                    weapon_affinity_dict["Story"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Story"] = [level.effectValue]
                                if "Colo" in weapon_affinity_dict:
                                    weapon_affinity_dict["Colo"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Colo"] = [level.effectValue]
                    else:
                        if "stage" in level.name:
                            if "+Area" in weapon_affinity_dict:
                                weapon_affinity_dict["+Area"][0] += level.effectValue
                            else:
                                weapon_affinity_dict["+Area"] = [level.effectValue]
                        else:
                            if level.cardDetailType != job.favoriteWeapon:
                                if WEAPON_INTEGER_VALUES[level.cardDetailType] not in weapon_affinity_dict[" "]:
                                    weapon_affinity_dict[" "] = weapon_affinity_dict[" "] + [WEAPON_INTEGER_VALUES[level.cardDetailType]]

                                weapon_index = weapon_affinity_dict[" "].index(WEAPON_INTEGER_VALUES[level.cardDetailType])

                                if "+Area" in weapon_affinity_dict:
                                    if len(weapon_affinity_dict["+Area"]) > 1:
                                        if len(weapon_affinity_dict["+Area"]) < weapon_index + 1:
                                            weapon_affinity_dict["+Area"] = weapon_affinity_dict["+Area"] + [level.effectValue]
                                        else:
                                            weapon_affinity_dict["+Area"][weapon_index] += level.effectValue
                                    else:
                                        weapon_affinity_dict["+Area"] = weapon_affinity_dict["+Area"] + [level.effectValue]
                                else:
                                    weapon_affinity_dict["+Area"] = [0, level.effectValue]

                                if "Story" in weapon_affinity_dict:
                                    if len(weapon_affinity_dict["Story"]) > 1:
                                        if len(weapon_affinity_dict["Story"]) < weapon_index + 1:
                                            weapon_affinity_dict["Story"] = weapon_affinity_dict["Story"] + [level.effectValue]
                                        else:
                                            weapon_affinity_dict["Story"][weapon_index] += level.effectValue
                                    else:
                                        weapon_affinity_dict["Story"] = weapon_affinity_dict["Story"] + [level.effectValue]
                                else:
                                    weapon_affinity_dict["Story"] = [0, level.effectValue]

                                if "Colo" in weapon_affinity_dict:
                                    if len(weapon_affinity_dict["Colo"]) > 1:
                                        if len(weapon_affinity_dict["Colo"]) < weapon_index + 1:
                                            weapon_affinity_dict["Colo"] = weapon_affinity_dict["Colo"] + [level.effectValue]
                                        else:
                                            weapon_affinity_dict["Colo"][weapon_index] += level.effectValue
                                    else:
                                        weapon_affinity_dict["Colo"] = weapon_affinity_dict["Colo"] + [level.effectValue]
                                else:
                                    weapon_affinity_dict["Colo"] = [0, level.effectValue]

                            else:
                                if "+Area" in weapon_affinity_dict:
                                    weapon_affinity_dict["+Area"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["+Area"] = [level.effectValue]
                                if "Story" in weapon_affinity_dict:
                                    weapon_affinity_dict["Story"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Story"] = [level.effectValue]
                                if "Colo" in weapon_affinity_dict:
                                    weapon_affinity_dict["Colo"][0] += level.effectValue
                                else:
                                    weapon_affinity_dict["Colo"] = [level.effectValue]

            weapon_affinity = "```" + tabulate(weapon_affinity_dict, headers='keys', tablefmt='pretty', colalign=["left", "center", "center"]) + "```"

            class_stats_dict = {}
            for level in job_levels:
                if level.effectType == 1:
                    if "HP" in class_stats_dict:
                        class_stats_dict["HP"] += level.effectValue
                    else:
                        class_stats_dict["HP"] = level.effectValue
                elif level.effectType == 2:
                    if "P.ATK" in class_stats_dict:
                        class_stats_dict["P.ATK"] += level.effectValue
                    else:
                        class_stats_dict["P.ATK"] = level.effectValue
                elif level.effectType == 3:
                    if "P.DEF" in class_stats_dict:
                        class_stats_dict["P.DEF"] += level.effectValue
                    else:
                        class_stats_dict["P.DEF"] = level.effectValue
                elif level.effectType == 4:
                    if "M.ATK" in class_stats_dict:
                        class_stats_dict["M.ATK"] += level.effectValue
                    else:
                        class_stats_dict["M.ATK"] = level.effectValue
                elif level.effectType == 5:
                    if "M.DEF" in class_stats_dict:
                        class_stats_dict["M.DEF"] += level.effectValue
                    else:
                        class_stats_dict["M.DEF"] = level.effectValue
                elif level.effectType == 7:
                    if "Cost" in class_stats_dict:
                        class_stats_dict["Cost"] += level.effectValue
                    else:
                        class_stats_dict["Cost"] = level.effectValue

            class_stats_ordered_list = ["HP", "P.ATK", "P.DEF", "M.ATK", "M.DEF", "Cost"]

            class_stats = ""
            for stat in class_stats_ordered_list:
                if stat in class_stats_dict:
                    class_stats += f"{stat}: +{class_stats_dict[stat]}\n"

            embed = Embed(title=job.name, description=job.description.replace("\\n", " "), type="rich", colour=color)
            embed.set_thumbnail(url=CLASS_IMAGE_URL.format(job.resourceName))
            embed.add_field(name="Levels", value=level_text, inline=False)
            embed.add_field(name="Weapon Affinity", value=weapon_affinity, inline=True)
            embed.add_field(name="Total Stats", value=class_stats, inline=True)
            embed.set_footer(text=f"Voice Actor: {job.characterVoice}")
            return embed


class SkillHelper:
    def __init__(self, skill):
        self.skill = skill

    def create_embed(self):
        skill = self.skill

        with session_scope() as s:
            description = skill.description.replace("\\n", " ")
            description += "\n\nWeapons with skill: "
            weapons_with_skill = list(set([
                weapon.name for weapon in s.query(Card).filter(or_(
                    Card.questSkillMstId==skill.skillMstId,
                    Card.frontSkillMstId==skill.skillMstId,
                    Card.autoSkillMstId==skill.skillMstId)).limit(20).all()
            ]))
        for weapon in weapons_with_skill:
            description += weapon + ", "
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

        return embed
