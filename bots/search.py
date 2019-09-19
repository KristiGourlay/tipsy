import pandas as pd


from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2


dbname = 'restaurant_info'
username = 'kristigourlay'
engine = 'postgres://%s@localhost/%s'%(username,dbname)




con = None
con = psycopg2.connect(database = dbname, user=username)


sql_query = """
SELECT * FROM restaurant_data;
"""

sql_query = """
SELECT *
FROM restaurant_data
WHERE restaurant_data.Hours == 8;
"""

r_df = pd.read_sql_query(sql_query,con)
r_df = r_df.rename(columns={'level_0': 'Names'})
r_df.append(fake_df, sort=True)
