import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

## restaurant_info is the database
## resaurant_data is the table

database_df = pd.read_csv('database_df.csv', index_col='Unnamed: 0')


# df.to_sql('restaurant_data', engine, if_exists='replace')


dbname = 'restaurant_info'
username = 'kristigourlay'
engine = 'postgres://%s@localhost/%s'%(username,dbname)


engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))

if not database_exists(engine.url):
    create_database(engine.url)

database_df.to_sql('restaurant_data', engine, if_exists='replace')






con = psycopg2.connect(engine)

cur = con.cursor()

sql_delete_query = """
Delete from restaurant_data WHERE restaurant_data.Hours > 1
"""

cur.execute(sql_delete_query)

#
# def add_to_db(data_frame):
#
#     dbname = 'restaurant_info'
#     username = 'kristigourlay'
#
#     engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
#
#     con = None
#     con = psycopg2.connect(database = dbname, user=username)
#
#     sql_query = """
#     SELECT * FROM restaurant_data;
#     """
#
#     r_df = pd.read_sql_query(sql_query,con)
#     r_df = r_df.rename(columns={'index': 'Names'})
#
#     data_frame = data_frame.rename(columns={'Unnamed: 0': 'Names'})
#     r_df.append(data_frame, sort=True)
#
#     return r_df.to_sql('restaurant_data', engine, if_exists='replace')


con = None
con = psycopg2.connect(database = dbname, user=username)


sql_query = """
SELECT * FROM restaurant_data;
"""

sql_query = """
SELECT restaurant_data.Hours FROM restaurant_data;
"""

r_df = pd.read_sql_query(sql_query,con)
r_df = r_df.rename(columns={'index': 'Names'})
r_df.append(fake_df, sort=True)



########

names = ['Kristi', 'Laura', 'Maruta', 'Siobhan', 'Jamie', 'Zac', 'Dell', 'Grace']


dbname = 'restaurant_info'
username = 'kristigourlay'
engine = 'postgres://%s@localhost/%s'%(username,dbname)

con = None
con = psycopg2.connect(database = dbname, user=username)


def search_by_name(name):

    return pd.read_sql_query(sql_query,con)


a = search_by_name()
a
