import pandas as pd
import flask
from flask import render_template, request
import json

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

import bots.database
from bots.database import add_to_db


import bots.split_day
from bots.split_day import final_function
from bots.split_day import make_compatible

import bots.regular
from bots.regular import final_func



# fake_df = pd.read_csv('fake_df.csv', index_col='Unnamed: 0')
# fake_df = fake_df.rename(columns={'tip_out': 'tip_envelope'})
# fake_df = fake_df.rename(columns={'Date': 'date', 'Hours': 'hours', 'Money_add': 'money_add'})
# fake_df
#
# fake_df.to_csv('database_df.csv')
# database_df = pd.read_csv('database_df.csv', index_col='Unnamed: 0')


app = flask.Flask(__name__)
#
# @app.route('/login')
# def login():
#     with open('templates/login.html', 'r') as login:
#         return login.read()


@app.route('/home')
def home():
    with open('templates/home.html', 'r') as home:
        return home.read()


@app.route('/page')
def page():
    with open('templates/page.html', 'r') as page:
        return page.read()

@app.route('/page2')
def page2():
    with open('templates/page2.html', 'r') as page2:
        return page2.read()

@app.route('/page3')
def page3():
    with open('templates/page3.html', 'r') as page3:
        return page3.read()


@app.route('/result', methods=['POST', 'GET'])
def result():
    if flask.request.method == 'POST':

        inputs = flask.request.form

        date = inputs['date']
        names = inputs['names']
        times = inputs['times']
        monies = inputs['monies']
        sold = inputs['sold']
        support = inputs['support']
        food_sales = inputs['food_sales']

        # database_df = pd.read_csv('database_df.csv')

        df = final_func(date, names, times, monies, sold, support, food_sales)


        database_df = pd.read_csv('database_df.csv', index_col='Unnamed: 0')
        database_df = database_df.append(df)
        database_df.to_csv('database_df.csv')

        add_to_db(database_df)


        return render_template('result.html', tables=[df.to_html(classes='data', header='true')])



@app.route('/result2', methods=['POST', 'GET'])
def result2():
    if flask.request.method == 'POST':

        inputs = flask.request.form

        date = inputs['date']
        names = inputs['names']
        day_hours = inputs['day_hours']
        sold = inputs['sold']
        food_sales = inputs['food_sales']
        night_hours = inputs['night_hours']
        monies = inputs['monies']
        day_sales = inputs['day_sales']
        day_support = inputs['day_support']
        night_support = inputs['night_support']

        df = final_function(date, names, day_hours, night_hours, monies, sold, day_sales, day_support, night_support, food_sales)

        database_df = pd.read_csv('database_df.csv', index_col='Unnamed: 0')
        df2 = make_compatible(df)
        database_df = database_df.append(df2)
        database_df.to_csv('database_df.csv')
        add_to_db(database_df)

        return render_template('result2.html', tables=[df.to_html(classes='data', header='true')])



@app.route('/database_home')
def database_home():
    with open('templates/database_home.html', 'r') as database_home:
        return database_home.read()


if __name__ == '__main__':
    '''Connects to the server'''

    HOST = '127.0.0.1'
    PORT = 4000

    app.run(HOST, PORT)
