import os
import pandas as pd

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager

from models import Base, Card, GuildToggle, Skill, CardEvolution, Item, LimitBreakSkill, Character, CharacterAbility, DiscordMessage, GuildMessageChannel
from constants import MASTER_URL, TABLE_LIST

db_url = "postgresql+psycopg2://postgres:llama555@localhost:5432/test_db"
#db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
engine = create_engine(db_url)

Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def recreate_database():
    Card.__table__.drop(engine)
    Skill.__table__.drop(engine)
    CardEvolution.__table__.drop(engine)
    Item.__table__.drop(engine)
    LimitBreakSkill.__table__.drop(engine)
    Character.__table__.drop(engine)
    CharacterAbility.__table__.drop(engine)
    DiscordMessage.__table__.drop(engine)

    Card.__table__.create(engine)
    Skill.__table__.create(engine)
    CardEvolution.__table__.create(engine)
    Item.__table__.create(engine)
    LimitBreakSkill.__table__.create(engine)
    Character.__table__.create(engine)
    CharacterAbility.__table__.create(engine)
    DiscordMessage.__table__.create(engine)
    GuildToggle.__table__.create(bind=engine, checkfirst=True)
    GuildMessageChannel.__table__.create(bind=engine, checkfirst=True)


def populate_database():
    list_of_string_columns = [
        'name', 
        'resourceName', 
        'description', 
        'characterUniqueName', 
        'characterVoice',
        'typeLabel',
        ]

    dict_dtypes = {x : 'str' for x in list_of_string_columns}

    for table in TABLE_LIST:
        data = pd.read_json(MASTER_URL.format(table["download_location"]), dtype=dict_dtypes)

        data_columns = list(data.columns)
        for column in data_columns:
            if column not in table["fields"]:
                data.drop(column, axis=1, inplace=True)

        with engine.begin() as connection:
            data.to_sql(table["name"], con=connection, if_exists='replace', method='multi')

    with session_scope() as s:
        skill_ids = [skill.skillMstId for skill in s.query(Skill).all()]

        for id in skill_ids:
            weapon = s.query(Card).filter(or_(
                Card.questSkillMstId==id,
                Card.frontSkillMstId==id,
                Card.autoSkillMstId==id)).first()

            if weapon is None:
                s.query(Skill).filter(Skill.skillMstId==id).delete()
