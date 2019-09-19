import pandas as pd
import flask
from flask import Flask, request, render_template
import json

def df_maker():
    names = input('Who worked?').split(',')
    times = input('How many hours?').split(',')
    monies = input('How much in tips?').split(',')
    new_times = []
    money = []
    for n in times:
        new_times.append(int(n))

    for m in monies:
        money.append(int(m))

    df = pd.DataFrame()
    df['Name'] = names
    df['Hours'] = new_times
    df['Money_add'] = money

    df = df.set_index('Name')
    return df


def final_func():
    sold = int(input('How much did the bar sell?'))
    support = int(input('How many support staff?'))
    food_sales = int(input('How much in food sales?'))
    df = df_maker()
    total_money = df.Money_add.sum()
    total_hours = df.Hours.sum()
    support_money = (sold * .01) * support
    kitchen_tipout = food_sales * .05
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


##split day


def df_maker2():
    names = input("who worked?").split(',')
    day_hours = (input('How many day hours?').split(','))
    night_hours = (input('How many night hours?').split(','))
    monies = (input('How much in tips?').split(','))

    new_day_times = []
    new_night_times = []
    money = []
    for n in day_hours:
        new_day_times.append(float(n))

    for nn in night_hours:
        new_night_times.append(float(nn))

    for m in monies:
        money.append(float(m))

    df2 = pd.DataFrame()
    df2['Names'] = names
    df2['Day_Hours'] = new_day_times
    df2['Night_Hours'] = new_night_times
    df2['Money_add'] = money

    df2 = df2.set_index('Names')

    return df2



def final_function():
    sold = float(input('How much did the bar sell?'))
    day_sales = float(input('What was the snapshot?'))
    day_support = int(input('How many support staff during the day?'))
    night_support = int(input('How many support staff during the night?'))
    food_sales = float(input('How much in food sales?'))
    df = df_maker2()
    night_sales = sold - day_sales


    total_money = df.Money_add.sum()
    total_day_hours = df.Day_Hours.sum()
    total_night_hours = df.Night_Hours.sum()


    day_support_money = (day_sales * .01) * day_support
    night_support_money = (night_sales * .01) * night_support

    kitchen_tipout = food_sales * .05
    total_money = total_money - kitchen_tipout

    day_money = (day_sales / sold) * total_money - day_support_money
    night_money = (night_sales / sold) * total_money - night_support_money

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



def tip_split():
    method = input('What type of split would you like?')
    if method == 'regular':
        results = final_func()
    if method == 'split_day':
        results = final_function()


    return results


#
# app = Flask(__name__)
#
# @app.route("/")
# def home():
#     return render_template('template/home.html')
#
# @app.route("/results")
# def tip_split():
#     method = input('What type of split would you like?')
#     if method == 'regular':
#         results = final_func()
#     if method == 'split_day':
#         results = final_function()
#
#     return results
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port='5000', debug=False)
