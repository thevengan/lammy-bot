# collection of constants used by the bot and supporting scripts

BOT_CHANNELS = ('bot-spam', 'spam-bot', 'bot-commands', 'bot-only', 'bots-only')

MASTER_URL = "https://raw.githubusercontent.com/sinoalice-datamine/data/master/EN/{}.json"

IMAGE_URL = "https://sinoalice.game-db.tw/images/cardL/CardL{}.png"

CLASS_IMAGE_URL = "https://sinoalice.game-db.tw/images/character_l/{}.png"

VERSION_URL = "https://raw.githubusercontent.com/sinoalice-datamine/data/master/EN/version.json"

WEAPON_ICON_URL = "https://drive.google.com/uc?export=view&id={}"

BUFF_SKILL_PRIMARY_ICON_VALUES = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

DEBUFF_SKILL_PRIMARY_ICON_VALUES = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

TABLE_LIST = [
    {
        "name": "card",
        "download_location" : "card_mst_list_en",
        "fields" : [
            "cardMstId",
            "questSkillMstId",
            "frontSkillMstId",
            "autoSkillMstId",
            "limitBreakSkillMstId",
            "name",
            "resourceName",
            "cardType",
            "weaponType",
            "rarity",
            "attribute",
            "maxLevel",
            "maxAttack",
            "maxMagicAttack",
            "maxDefence",
            "maxMagicDefence",
            "evolutionLevel",
            "deckCost",
            "isInfiniteEvolution",
            "isParameterCustomEnabled",
            "isSkillCustomEnabled",
            "isRelease",
        ]
    },
    {
        "name" : "cardEvolution",
        "download_location" : "card_evolution_mst_list",
        "fields" : [
            "cardEvolutionMstId",
            "cardMstId",
            "evolvedCardMstId",
            "money",
            "itemMstId1",
            "itemMstNum1",
            "itemMstId2",
            "itemMstNum2",
            "itemMstId3",
            "itemMstNum3",
            "itemMstId4",
            "itemMstNum4",
            "itemMstId5",
            "itemMstNum5",
        ]
    },
    {
        "name" : "item",
        "download_location" : "item_mst_list",
        "fields" : [
            "itemMstId",
            "name",
        ]
    },
    {
        "name" : "skill",
        "download_location" : "skill_mst_list",
        "fields" : [
            "skillMstId",
            "category",
            "name",
            "description",
            "sp",
            "typeLabel",
            "primaryIcon",
            "rangeIcon",
        ]
    },
    {
        "name" : "limitBreakSkill",
        "download_location" : "limit_break_skill_mst_list",
        "fields" : [
            "limitBreakSkillMstId",
            "name",
            "description",
        ]
    },
    {
        "name" : "character",
        "download_location" : "character_mst_list",
        "fields" : [
            "characterMstId",
            "name",
            "characterUniqueName",
            "rolePosition",
            "description",
            "favoriteWeapon",
            "resourceName",
            "characterVoice",
            "displayStartTime",
        ]
    },
    {
        "name" : "characterAbility",
        "download_location" : "character_ability_mst_list",
        "fields" : [
            "characterAbilityMstId",
            "characterMstId",
            "name",
            "releaseLevel",
            "skillType",
            "effectType",
            "effectValue",
            "cardDetailType",
        ]
    },
    {
        "name" : "characterStory",
        "download_location" : "character_story_mst_list",
        "fields" : [
            "characterStoryMstId",
            "characterMstId",
            "releaseLevel",
            "story",
        ]
    },
]

WEAPON_INTEGER_VALUES = {
    1: "Instrument",
    2: "Tome",
    3: "Artifact",
    4: "Staff",
    5: "Blade",
    6: "Heavy",
    7: "Projectile",
    8: "Polearm",
}

HELP_MESSAGE = """**Available Commands**
**Prefix** - use `!soa[command]` to access bot commands - eg. `!soahowto`
- `howto` : sends a DM to the message author detailing the commands available.

- `initialize` : creates the necessary channels and roles for `lammy-bot` to function.
      - what this entails - creates `sino_conquest`, `sino_guerrilla`, and `sino_purification` as server roles. Creates the `bot-spam` channel for using other commands.

- `giverole [role]` : gives the message author the requested role(s). Multiple roles can be given by separating them with a `space`. Possible roles are `conquest, guerrilla, purification`.
      - example - `!soagiverole conquest guerrilla` would give the message author the `sino_conquest` and `sino_guerrilla` roles.

- `removerole [role]` : removes the requested role(s) from the message author. Multiple roles can be given by separating them with a `space`. Possible roles are `conquest, guerrilla, purification`.
      - example - `!soaremoverole purification` would remove the `sino_purification` role from the message author.

- `toggle [@mention]` : toggles the requested @mention for the current server. Multiple @mentions can be given by separating them with a `space`. Possible @mentions are `conquest, guerrilla, purification`. You can turn off an @mention at the same time you turn another @mention off.
    - example - `!soatoggle guerrilla conquest` would toggle the @mentions for the `sino_guerrilla` and `sino_conquest` roles for the current server.

- `channel [channel_name]` : sets a custom channel for `lammy-bot` to listen for commands in. You can then delete any channels created by/for `lammy-bot`.
    - example - `!soachannel sino-bots` would look for the channel `sino-bots` in your server and, if it exists, set as a channel that you can use `lammy-bot` with.
    """

HELP_MESSAGE_CONT = """- `weapon [weapon]`: searches the weapon database for the text entered after the command and returns an embed with information on the most relevant weapon.
      - example - `!soaweapon entrail` would pull up an embed with information for `Entrails of Justice`.

- `skill [skill]` : searches the skill database for the text entered after the command and returns an embed with information on the most relevant skill.
      - example - `!soaskill hero's harmony` would pull up an embed with information for `Hero's Harmony (I)`.

- `nightmare [nightmare]` : searches the nightmare database for the text entered after the command and returns an embed with information on the most relevant nightmare.
      - example `!soanightmare uga` would pull up an embed with information for `Ugallu`.

- `job [character]/[job]` : searches the jon database for the text entered after the command and returns an embed with information on the most relevant job.
      - example `!soajob three little pigs/min` would pull up an embed with information for `Three Little Pigs/Minstrel`.
      - this command can take shortened character and job names as long as they are part of the whole name.
        - `!soajob red/lust` would work, but neither `!soajob rrh/lust` nor `!soajob red/l scorp` would work."""

PRIVACY_POLICY_MESSAGE = """
This bot keeps track of the following Discord Server information:
 - Server ID (for keeping track of your server-specific settings)
 - Channel IDs (for keeping track of which channel lammy-bot is listening for commands in)
 - Message IDs (for enabling lammy-bot to edit messages)

This bot **DOES NOT** keep track of any personal information, or any personal Discord User IDs.

All server information is stored on a secured database server that only Vengan#7777 has access to.

If you have any concerns, or if you would like your data removed, please contact Vengan#7777.
"""
