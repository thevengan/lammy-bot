from nextcord import ButtonStyle, Interaction, SelectOption
from nextcord.ui import button, Button, Select, View

from datetime import datetime

from crud import session_scope
from embed_helper import NightmareHelper, SkillHelper, WeaponHelper
from models import Card, CardEvolution, DiscordMessage, Skill

class WeaponView(View):
    def __init__(self):
        super().__init__()

        self.devolve.disabled = True

    @button(label="Devolve", style=ButtonStyle.gray)
    async def devolve(self, button: Button, interaction: Interaction):
        with session_scope() as s:
            message_id = interaction.message.id

            message_meta_data = s.query(DiscordMessage).filter(DiscordMessage.message_id==message_id).first()

            prev = message_meta_data.prev
            weapon = s.query(Card).filter(Card.cardMstId==prev).first()
            helper = WeaponHelper(weapon)
            embed = helper.create_embed()

            devolution = s.query(CardEvolution).filter(CardEvolution.evolvedCardMstId==prev).first()

            message_meta_data.last_updated = datetime.now()
            message_meta_data.next = message_meta_data.curr
            message_meta_data.curr = message_meta_data.prev
            message_meta_data.prev = devolution.cardMstId if devolution else None

            self.evolve.disabled = False
            if devolution:
                self.devolve.disabled = False
            else:
                self.devolve.disabled = True

            await interaction.response.edit_message(embed=embed, view=self)

    @button(label="Evolve", style=ButtonStyle.gray)
    async def evolve(self, button: Button, interaction: Interaction):
        with session_scope() as s:
            message_id = interaction.message.id

            message_meta_data = s.query(DiscordMessage).filter(DiscordMessage.message_id==message_id).first()

            next = message_meta_data.next
            weapon = s.query(Card).filter(Card.cardMstId==next).first()
            helper = WeaponHelper(weapon)
            embed = helper.create_embed()

            evolution = s.query(CardEvolution).filter(CardEvolution.cardMstId==next).first()

            message_meta_data.last_updated = datetime.now()
            message_meta_data.prev = message_meta_data.curr
            message_meta_data.curr = message_meta_data.next
            message_meta_data.next = evolution.evolvedCardMstId if evolution else None

            self.devolve.disabled = False
            if evolution:
                self.evolve.disabled = False
            else:
                self.evolve.disabled = True

            await interaction.response.edit_message(embed=embed, view=self)


class NightmareView(View):
    def __init__(self):
        super().__init__()

        self.devolve.disabled = True

    @button(label="Devolve", style=ButtonStyle.gray)
    async def devolve(self, button: Button, interaction: Interaction):
        with session_scope() as s:
            message_id = interaction.message.id

            message_meta_data = s.query(DiscordMessage).filter(DiscordMessage.message_id==message_id).first()

            prev = message_meta_data.prev
            nightmare = s.query(Card).filter(Card.cardMstId==prev).first()
            helper = NightmareHelper(nightmare)
            embed = helper.create_embed()

            devolution = s.query(CardEvolution).filter(CardEvolution.evolvedCardMstId==prev).first()

            message_meta_data.last_updated = datetime.now()
            message_meta_data.next = message_meta_data.curr
            message_meta_data.curr = message_meta_data.prev
            message_meta_data.prev = devolution.cardMstId if devolution else None

            self.evolve.disabled = False
            if devolution:
                self.devolve.disabled = False
            else:
                self.devolve.disabled = True

            await interaction.response.edit_message(embed=embed, view=self)

    @button(label="Evolve", style=ButtonStyle.gray)
    async def evolve(self, button: Button, interaction: Interaction):
        with session_scope() as s:
            message_id = interaction.message.id

            message_meta_data = s.query(DiscordMessage).filter(DiscordMessage.message_id==message_id).first()

            next = message_meta_data.next
            nightmare = s.query(Card).filter(Card.cardMstId==next).first()
            helper = NightmareHelper(nightmare)
            embed = helper.create_embed()

            evolution = s.query(CardEvolution).filter(CardEvolution.cardMstId==next).first()

            message_meta_data.last_updated = datetime.now()
            message_meta_data.prev = message_meta_data.curr
            message_meta_data.curr = message_meta_data.next
            message_meta_data.next = evolution.evolvedCardMstId if evolution else None

            self.devolve.disabled = False
            if evolution:
                self.evolve.disabled = False
            else:
                self.evolve.disabled = True

            await interaction.response.edit_message(embed=embed, view=self)


class SkillDropdown(Select):
    def __init__(self, options: list[SelectOption]):
        super().__init__(placeholder="Other SP Costs", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        with session_scope() as s:
            uid = self.values[0].split()[2][:-1]

            skill = s.query(Skill).filter(Skill.skillMstId==uid, Skill.category!=4).first()

            helper = SkillHelper(skill)
            embed = helper.create_embed()

            await interaction.response.edit_message(embed=embed)


class SkillView(View):
    def __init__(self, dropdown: Select):
        super().__init__()
        self.add_item(dropdown)

