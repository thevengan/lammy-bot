from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean


Base = declarative_base()

class Card(Base):
    __tablename__ = 'card'
    cardMstId = Column(Integer, primary_key=True)
    questSkillMstId = Column(Integer)
    frontSkillMstId = Column(Integer)
    autoSkillMstId = Column(Integer)
    name = Column(String)
    resourceName = Column(String)
    weaponType = Column(Integer)
    rarity = Column(Integer)
    attribute = Column(Integer)
    maxLevel = Column(Integer)
    maxAttack = Column(Integer)
    maxMagicAttack = Column(Integer)
    maxDefence = Column(Integer)
    maxMagicDefence = Column(Integer)
    evolutionLevel = Column(Integer)
    deckCost = Column(Integer)
    isInfiniteEvolution = Column(Boolean)
    isParameterCustomEnabled = Column(Boolean)
    isSkillCustomEnabled = Column(Boolean)

class CardEvolution(Base):
    __tablename__ = 'cardEvolution'
    cardEvolutionMstId = Column(Integer, primary_key=True)
    cardMstId = Column(Integer)
    evolvedCardMstId = Column(Integer)
    money = Column(Integer)
    itemMstId1 = Column(Integer)
    itemMstNum1 = Column(Integer)
    itemMstId2 = Column(Integer)
    itemMstNum2 = Column(Integer)
    itemMstId3 = Column(Integer)
    itemMstNum3 = Column(Integer)
    itemMstId4 = Column(Integer)
    itemMstNum4 = Column(Integer)
    itemMstId5 = Column(Integer)
    itemMstNum5 = Column(Integer)

class Item(Base):
    __tablename__ = 'item'
    itemMstId = Column(Integer, primary_key=True)
    name = Column(String)

class Skill(Base):
    __tablename__ = 'skill'
    skillMstId = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    sp = Column(Integer)
    typeLabel = Column(Integer)

class LimitBreakSkill(Base):
    __tablename__ = 'limitBreakSkill'
    limitBreakSkillMstId = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

class Character(Base):
    __tablename__ = 'character'
    characterMstId = Column(Integer, primary_key=True)
    name = Column(String)
    characterUniqueName = Column(String)
    rolePosition = Column(Integer)
    description = Column(String)
    favoriteWeapon = Column(Integer)
    resourceName = Column(String)
    characterVoice = Column(String)

class CharacterAbility(Base):
    __tablename__ = 'characterAbility'
    characterAbilityMstId = Column(Integer, primary_key=True)
    characterMstId = Column(Integer)
    name = Column(String)
    releaseLevel = Column(Integer)