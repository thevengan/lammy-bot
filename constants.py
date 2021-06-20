# collection of constants used by the bot and supporting scripts

BOT_CHANNELS = ('bot-spam', 'spam-bot')

MASTER_URL = "https://raw.githubusercontent.com/sinoalice-datamine/data/master/EN/{}.json"

IMAGE_URL = "https://sinoalice.game-db.tw/images/cardL/CardL{}.png"

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
            "isSkillCustomEnabled"
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
            "itemMstNum5"
        ]
    },
    {
        "name" : "item",
        "download_location" : "item_mst_list",
        "fields" : [
            "itemMstId",
            "name"
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
            "rangeIcon"
        ]
    },
    {
        "name" : "limitBreakSkill",
        "download_location" : "limit_break_skill_mst_list",
        "fields" : [
            "limitBreakSkillMstId",
            "name",
            "description"
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
            "characterVoice"
        ]
    },
    {
        "name" : "characterAbility",
        "download_location" : "character_ability_mst_list",
        "fields" : [
            "characterAbilityMstId",
            "characterMstId",
            "name",
            "releaseLevel"
        ]
    }
]