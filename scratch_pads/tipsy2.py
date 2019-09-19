import pandas as pd
import numpy as np



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


final_func()
