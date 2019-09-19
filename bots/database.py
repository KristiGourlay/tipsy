import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

## restaurant_info is the database
## resaurant_data is the table

def add_to_db(dataframe):

    dbname = 'restaurant_info'
    username = 'kristigourlay'
    engine = 'postgres://%s@localhost/%s'%(username,dbname)

    return dataframe.to_sql('restaurant_data', engine, if_exists='replace')
