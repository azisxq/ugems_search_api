import os
import pandas as pd
from sqlalchemy import create_engine

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
    )
)


def get_token(token, engine=engine):
	statement = f"select * from api_solr_token where token = '{token}'"
	cek_token = pd.read_sql_query(statement, engine)
	if (len(cek_token)>0):
        return cek_token['name'][0]
    else:
        return None