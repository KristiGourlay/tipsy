import pandas as pd

# date = 'Aug 24 19'
# names = 'Kristi, Laura, Sofia, Grace, Dell'
# times = '8, 6, 4, 5, 6'
# monies = '200, 210, 120, 150, 180'
# sold = 8700
# support = 1
# food_sales = 3000



def final_func(date, names, times, monies, sold, support, food_sales):
    new_times = []
    money = []
    name_list = []
    date = str(date)

    for n in times.split(','):
        new_times.append(float(n))

    for m in monies.split(','):
        money.append(float(m))

    for name in names.split(','):
        name_list.append(name)

    df = pd.DataFrame()
    df['names'] = name_list
    df['hours'] = new_times
    df['money_add'] = money
    df['date'] = date


    df = df.set_index('names')

    total_money = df.money_add.sum()
    total_hours = df.hours.sum()
    support_money = (float(sold) * .01) * float(support)
    kitchen_tipout = float(food_sales) * .05
    total_money = total_money - support_money - kitchen_tipout
    hourly = total_money/total_hours

    sup = pd.DataFrame(['NA'] * 4).T
    sup.columns = ['date', 'hours', 'money_add', 'tip_envelope']
    sup['tip_envelope'] = support_money

    kit = pd.DataFrame(['NA'] * 4).T
    kit.columns = sup.columns
    kit['tip_envelope'] = kitchen_tipout

    df['tip_envelope'] = df.hours * hourly
    df = df.append(sup)
    df = df.rename(index={0: "support_money"})
    df = df.append(kit)
    df = df.rename(index={0: "kitchen_tip"})
    df['date'] = date


    return df
