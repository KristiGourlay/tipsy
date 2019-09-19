import pandas as pd
import numpy as np



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

names = 'Kristi, Maruta, Laura, Jamie, Siobhan'
day_hours = '8, 8, 6, 4, 1'
night_hours = '0, 0, 3, 5, 8'
monies = '140, 150, 180, 210, 240'
sold = 6000
day_sales = 4000
day_support = 1
night_support = 1
food_sales = 1300
df1 = final_function(names, day_hours, night_hours, monies, sold, day_sales, day_support, night_support, food_sales)
