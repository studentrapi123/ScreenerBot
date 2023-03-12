import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import matplotlib.dates as mpl_dates
from creds import user, password

def get_stock_price(symbol, tf):
    if not mt5.initialize(login=user, password=password, server="FTMO-Demo"):
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    if tf == "1W":
        df = mt5.copy_rates_from_pos((symbol), mt5.TIMEFRAME_W1, 0, 2000)
    if tf == "1D":
        df = mt5.copy_rates_from_pos((symbol), mt5.TIMEFRAME_D1, 0, 2000)
    if tf == "4H":
        df = mt5.copy_rates_from_pos((symbol), mt5.TIMEFRAME_H4, 0, 400)
    if tf == "1H":
        df = mt5.copy_rates_from_pos((symbol), mt5.TIMEFRAME_H1, 0, 400)

    df = pd.DataFrame(df)

    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['time'] = df['time'].apply(mpl_dates.date2num)

    df = df.loc[:,['time', 'open', 'high', 'low', 'close']]

    return df

def is_support(df,i):
    cond1 = df['low'][i] < df['low'][i-1]
    cond2 = df['low'][i] < df['low'][i+1]
    cond3 = df['low'][i+1] < df['low'][i+2]
    cond4 = df['low'][i-1] < df['low'][i-2]
    return (cond1 and cond2 and cond3 and cond4)
    # determine bearish fractal

def is_resistance(df,i):
    cond1 = df['high'][i] > df['high'][i-1]
    cond2 = df['high'][i] > df['high'][i+1]
    cond3 = df['high'][i+1] > df['high'][i+2]
    cond4 = df['high'][i-1] > df['high'][i-2]
    return (cond1 and cond2 and cond3 and cond4)
    # to make sure the new level area does not exist already

def is_far_from_level(value, levels, df):
    ave = np.mean(df['high'] - df['low'])
    return np.sum([abs(value-level)<ave for _,level in levels])==0

# a list to store resistance and support levels
def support_res_print(symbol, tf):

    df = get_stock_price(symbol, tf)

    levels = []
    for i in range(2, df.shape[0] - 2):
        if is_support(df, i):
            low = df['low'][i]
            if is_far_from_level(low, levels, df):
                levels.append((i, low))
        elif is_resistance(df, i):
            high = df['high'][i]
            if is_far_from_level(high, levels, df):
                levels.append((i, high))

    copy_res = []

    for level in levels:
        copy_res.append(float(level[1]))

    copy_res.sort()

    return (copy_res)

def support_res_return_swing(symbol, tf):
    df = get_stock_price(symbol, tf)

    levels = []
    for i in range(2, df.shape[0] - 2):
        if is_support(df, i):
            low = df['low'][i]
            if is_far_from_level(low, levels, df):
                levels.append((i, low))
        elif is_resistance(df, i):
            high = df['high'][i]
            if is_far_from_level(high, levels, df):
                levels.append((i, high))

    copy_res = []

    for level in levels:
        copy_res.append(float(level[1]))

    #print(copy_res, symbol)

    close = float(df["close"].tail(1))

    closest_value = min(copy_res, key=lambda x:abs(x-close))

    percent_change = ((closest_value-close)/close)*100

    return (percent_change, closest_value)

symbol = "USDCHF"

def replaceSR(mystring, tf):
    start = mystring.find("{")
    end = mystring.find("}")

    if start != -1 and end != -1:
        result1 = mystring[0:start+1]
        result2 = mystring[end:-1]

        SR = support_res_print(symbol, tf)
        SR_LIST = ",".join([str(i) for i in SR])

        result = result1+(SR_LIST)+result2
        return (result)

save_string = ""
remove_whitespace = ""

with open("C:/Users/nikit/AppData/Roaming/MetaQuotes/Terminal/49CDDEAA95A409ED22BD2287BB67CB9C/MQL5/Experts/Support_Resistance_Single.mq5","r") as f:
    for i in f.readlines():
        if not i.strip():
            continue
        if i:
            remove_whitespace = (remove_whitespace+i+"\n")
f.close()

f = open("C:/Users/nikit/AppData/Roaming/MetaQuotes/Terminal/49CDDEAA95A409ED22BD2287BB67CB9C/MQL5/Experts/Support_Resistance_Single.mq5","w+")
f.writelines(remove_whitespace)
f.close()

with open("C:/Users/nikit/AppData/Roaming/MetaQuotes/Terminal/49CDDEAA95A409ED22BD2287BB67CB9C/MQL5/Experts/Support_Resistance_Single.mq5", "r", encoding="cp1252") as f:
    for line in f:
        if "Supports1W[]" in line:
            replace = replaceSR(line, "1W")
            save_string = (save_string+replace+"\n")

        elif "Supports1D[]" in line:
            replace = replaceSR(line, "1D")
            save_string = (save_string+replace+"\n")
        else:
            save_string = (save_string+line+"\n")

f.close()

f = open("C:/Users/nikit/AppData/Roaming/MetaQuotes/Terminal/49CDDEAA95A409ED22BD2287BB67CB9C/MQL5/Experts/Support_Resistance_Single.mq5","w+")
f.writelines(save_string)
f.close()