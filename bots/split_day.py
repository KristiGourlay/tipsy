import pandas as pd

#
# date = 'Aug 24 19'
# names = 'Kristi, Laura, Sofia, Grace, Dell'
# day_hours = '8, 8, 3, 0, 0'
# night_hours = '0, 0, 5, 8, 8'
# monies = '200, 210, 120, 150, 180'
# sold = 8700
# day_sales = 4100
# day_support = 1
# night_support = 1
# food_sales = 3000
#
#


def final_function(date, names, day_hours, night_hours, monies, sold, day_sales, day_support, night_support, food_sales):

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
    df['names'] = name_list
    df['day_hours'] = new_day_times
    df['night_hours'] = new_night_times
    df['money_add'] = money
    df['date'] = date

    df = df.set_index('names')

    night_sales = float(sold) - float(day_sales)

    total_money = df.money_add.sum()
    total_day_hours = df.day_hours.sum()
    total_night_hours = df.night_hours.sum()

    day_support_money = (float(day_sales) * .01) * float(day_support)
    night_support_money = (float(night_sales) * .01) * float(night_support)

    kitchen_tipout = float(food_sales) * .05
    total_money = float(total_money) - float(kitchen_tipout)

    day_money = (float(day_sales) / float(sold)) * total_money - day_support_money
    night_money = (float(night_sales) / float(sold)) * total_money - night_support_money

    day_hourly = day_money/total_day_hours
    night_hourly = night_money/total_night_hours

    df['tip_envelope'] = (df.day_hours * day_hourly) + (df.night_hours * night_hourly)

    sup = pd.DataFrame(['NA'] * 5).T
    sup.columns = ['date', 'day_hours', 'night_hours', 'money_add', 'tip_envelope']
    sup['tip_envelope'] = day_support_money

    sup2 = pd.DataFrame(['NA'] * 5).T
    sup2.columns = sup.columns
    sup2['tip_envelope'] = night_support_money


    kit = pd.DataFrame(['NA'] * 5).T
    kit.columns = sup.columns
    kit['tip_envelope'] = kitchen_tipout

    df = df.append(sup)
    df = df.rename(index={0: "day_support_money"})
    df = df.append(sup2)
    df = df.rename(index={0: "night_support_money"})
    df = df.append(kit)
    df = df.rename(index={0: "kitchen_tip"})
    df['date'] = date

    return df




def make_compatible(data_frame):
    data_frame['hours'] = data_frame.day_hours + data_frame.night_hours
    data_frame = data_frame.replace('NANA', "NA")
    data_frame = data_frame.drop(columns=['day_hours', 'night_hours'])

    return data_frame
