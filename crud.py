import os
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager

from models import Base
from constants import MASTER_URL, TABLE_LIST


db_url = os.getenv("DATABASE_URL")
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
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def populate_database():
    list_of_string_columns = [
        'name', 
        'resourceName', 
        'description', 
        'characterUniqueName', 
        'characterVoice'
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
