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


def final_function(names, day_hours, night_hours, monies, sold, day_sales, day_support, night_support, food_sales):

    new_day_times = []
    new_night_times = []
    name_list = []
    money = []
    for n in day_hours.split(','):
        new_day_times.append(float(n))

    for nn in night_hours.split(','):
        new_night_times.append(float(nn))

    for m in monies.split(','):
        money.append(float(m))

    for name in names.split(','):
        name_list.append(name)

    df = pd.DataFrame()
    df['Names'] = name_list
    df['Day_Hours'] = new_day_times
    df['Night_Hours'] = new_night_times
    df['Money_add'] = money

    df = df.set_index('Names')

    night_sales = float(sold) - float(day_sales)

    total_money = df.Money_add.sum()
    total_day_hours = df.Day_Hours.sum()
    total_night_hours = df.Night_Hours.sum()

    day_support_money = (float(day_sales) * .01) * float(day_support)
    night_support_money = (float(night_sales) * .01) * float(night_support)

    kitchen_tipout = float(food_sales) * .05
    total_money = float(total_money) - float(kitchen_tipout)

    day_money = (float(day_sales) / float(sold)) * total_money - day_support_money
    night_money = (float(night_sales) / float(sold)) * total_money - night_support_money

    day_hourly = day_money/total_day_hours
    night_hourly = night_money/total_night_hours

    df['tip_envelope'] = (df.Day_Hours * day_hourly) + (df.Night_Hours * night_hourly)

    sup = pd.DataFrame(['NA'] * 4).T
    sup.columns = ['Day_Hours', 'Night_Hours', 'Money_add', 'tip_envelope']
    sup['tip_envelope'] = day_support_money

    sup2 = pd.DataFrame(['NA'] * 4).T
    sup2.columns = ['Day_Hours', 'Night_Hours', 'Money_add', 'tip_envelope']
    sup2['tip_envelope'] = night_support_money


    kit = pd.DataFrame(['NA'] * 4).T
    kit.columns = sup.columns
    kit['tip_envelope'] = kitchen_tipout

    df = df.append(sup)
    df = df.rename(index={0: "Day_support_money"})
    df = df.append(sup2)
    df = df.rename(index={0: "Night_support_money"})
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

@app.route('/result2', methods=['POST', 'GET'])
def result2():
    if flask.request.method == 'POST':

        inputs = flask.request.form

        names = inputs['names']
        day_hours = inputs['day_hours']
        sold = inputs['sold']
        food_sales = inputs['food_sales']
        night_hours = inputs['night_hours']
        monies = inputs['monies']
        day_sales = inputs['day_sales']
        day_support = inputs['day_support']
        night_support = inputs['night_support']

        df = final_function(names, day_hours, night_hours, monies, sold, day_sales, day_support, night_support, food_sales)

        return render_template('result2.html', tables=[df.to_html(classes='data', header='true')])

if __name__ == '__main__':
    '''Connects to the server'''

    HOST = '127.0.0.1'
    PORT = 4000

    app.run(HOST, PORT)
