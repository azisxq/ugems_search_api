import os
import pandas as pd
from sqlalchemy import create_engine
from uuid import uuid4
from datetime import datetime

postgres_host = os.environ['POSTGRES_HOST']
postgres_port = os.environ['POSTGRES_PORT']
postgres_user = os.environ['POSTGRES_USER']
postgres_pass = os.environ['POSTGRES_PASS']
postgres_db = os.environ['POSTGRES_DB']

engine = create_engine(
    "postgresql://{}:{}@{}:{}/{}".format(
        postgres_user,
        postgres_pass,
        postgres_host,
        postgres_port ,
        postgres_db,
    ),
    connect_args={'connect_timeout': 100}
)


def search_token(token, engine=engine):
    statement = f"select * from api_solr_token where token = '{token}'"
    cek_token = pd.read_sql_query(statement, engine)
    if (len(cek_token)>0):
        return cek_token['name'][0]
    else:
        return None


def create_token(engine=engine):
    rand_token = str(uuid4())
    date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    token_df = {
        "name" : ['Solr_token'],
        "token": [rand_token],
        "last_update":[date_time]
    }
    token_pd = pd.DataFrame(token_df)
    token_pd.to_sql('api_solr_token', engine, index=False, if_exists='replace',method="multi")


def get_token(engine=engine):
    statement = "select token from api_solr_token"
    cek_token = pd.read_sql_query(statement, engine)
    return cek_token['token'][0]