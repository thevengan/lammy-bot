MASTER_URL = "https://raw.githubusercontent.com/sinoalice-datamine/data/master/EN/{}.json"
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
            "name",
            "description",
            "sp",
            "typeLabel"
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