import pandas as pd
import flask
from flask import render_template
import json

app = flask.Flask(__name__)


def final_func(names, times, monies, sold, support, food_sales):
    new_times = []
    money = []
    name_list = []

    for n in times.split(','):
        new_times.append(float(n))

    for m in monies.split(','):
        money.append(float(m))

    for name in names.split(','):
        name_list.append(name)

    df = pd.DataFrame()
    df['Name'] = name_list
    df['Hours'] = new_times
    df['Money_add'] = money

    df = df.set_index('Name')

    total_money = df.Money_add.sum()
    total_hours = df.Hours.sum()
    support_money = (float(sold) * .01) * float(support)
    kitchen_tipout = float(food_sales) * .05
    total_money = total_money - support_money - kitchen_tipout
    hourly = total_money/total_hours

    sup = pd.DataFrame(['NA'] * 3).T
    sup.columns = ['Hours', 'Money_add', 'tip_out']
    sup['tip_out'] = support_money

    kit = pd.DataFrame(['NA'] * 3).T
    kit.columns = sup.columns
    kit['tip_out'] = kitchen_tipout

    df['tip_out'] = df.Hours * hourly
    df = df.append(sup)
    df = df.rename(index={0: "Support_money"})
    df = df.append(kit)
    df = df.rename(index={0: "kitchen_tip"})

    return df


#-------- ROUTES GO HERE -----------#

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

@app.route('/result', methods=['POST', 'GET'])
def result():
    if flask.request.method == 'POST':

        inputs = flask.request.form

        names = inputs['names']
        times = inputs['times']
        monies = inputs['monies']
        sold = inputs['sold']
        support = inputs['support']
        food_sales = inputs['food_sales']

        df = final_func(names, times, monies, sold, support, food_sales)

        return render_template('result.html', tables=[df.to_html(classes='data', header='true')])



if __name__ == '__main__':
    '''Connects to the server'''

    HOST = '127.0.0.1'
    PORT = 4000

    app.run(HOST, PORT)
