from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd
import talib
import pandas_ta as ta
from datetime import datetime, timedelta
import time
from discordwebhook import Discord
from creds import user, password

def end_of_day(tf):
    symbols = mt5.symbols_get(group="*,!GOOG, !FB, !NFLX, !NVDA, !META, !VOWG_p, !DBKGn, !LVMH, !MSFT, !BABA, !BAC, !ALVG, !AAPL, !WMT, !V, !BAYGn, !IBE, !ERBN.f, !AMZN, !TSLA, !ZM")
    time.sleep(1)

    for s in symbols:
        if tf == "15m":
            rates = mt5.copy_rates_from_pos(str(s.name), mt5.TIMEFRAME_M15, 0, 100)
            discord = Discord(
            url="https://discordapp.com/api/webhooks/1034934795941199882/ZlL6Jvcy4w092NYMVSNBVrL-VQnWO0QwKFWWzLE-h7bdo30ML_CWTJsFb4tVljOTO2yu")

        ticker = pd.DataFrame(rates)
        ticker['time'] = pd.to_datetime(ticker['time'], unit='s')

        ticker['10 MA'] = ticker["close"].rolling(window=10).mean()
        ticker['5 MA'] = ticker["close"].rolling(window=5).mean()


def round_dt(dt, delta):
    return datetime.min + round((dt - datetime.min) / delta) * delta

def fifteen_minute_full_candle_check(tf):
    symbols = mt5.symbols_get(group="*,!GOOG, !FB, !NFLX, !NVDA, !META, !VOWG_p, !DBKGn, !LVMH, !MSFT, !BABA, !BAC, !ALVG, !AAPL, !WMT, !V, !BAYGn, !IBE, !ERBN.f, !AMZN, !TSLA, !ZM")

    time.sleep(1)

    for s in symbols:
        try:
            if tf == "1m":
                rates = mt5.copy_rates_from_pos(str(s.name), mt5.TIMEFRAME_M1, 0, 300)
                minutes_to_add = 1
                discord = Discord(url="https://discordapp.com/api/webhooks/1042785617056124999/lry2isyY3BlntQsbImSm8o3nbwn7EgDdWn1axyCeskXudcMy7IdczRkUok0hXEaGIzhL")
            if tf == "15m":
                rates = mt5.copy_rates_from_pos(str(s.name), mt5.TIMEFRAME_M15, 0, 300)
                minutes_to_add = 15
                discord = Discord(url="https://discordapp.com/api/webhooks/1014902093708009573/ZY614TwqlNvcTxi8o5XdqrRX5VKBqB6zzjTWwsWWL6jEyAkCLLGMPus_aSPA5lrxYZLD")
            if tf == "1h":
                rates = mt5.copy_rates_from_pos(str(s.name), mt5.TIMEFRAME_H1, 0, 300)
                minutes_to_add = 60
                discord = Discord(url="https://discordapp.com/api/webhooks/1014902020500631603/yTRIVJ3i77EZ_Lg7Kvyh71YUFI9UTuDr38ixk9T1hhbbAYKB7vVcH9I6rVNB91XyecI8")
            if tf == "4h":
                rates = mt5.copy_rates_from_pos(str(s.name), mt5.TIMEFRAME_H4, 0, 300)
                minutes_to_add = 240
                discord = Discord(url="https://discordapp.com/api/webhooks/1014901586591481919/U5mO_ZOhaNUeG4a4uQBHUO7NH2LB9KDJzgBfuTGjp63ZkWUZ1ljP5SKkpi-AHWsq0KsR")
            if tf == "1d":
                rates = mt5.copy_rates_from_pos(str(s.name), mt5.TIMEFRAME_D1, 0, 300)
                minutes_to_add = 1440
                discord = Discord(url="https://discordapp.com/api/webhooks/1029452372474343484/c6WTS48PLGEPeT8CFzJCDZ-3SEcsOYZ-MCUIm3UqUF5p1bORq2pbgVlNz90C4tT7xnlO")

            ticker = pd.DataFrame(rates)
            ticker['time'] = pd.to_datetime(ticker['time'], unit='s')

            ticker['Upper Band'], ticker['Middle Band'], ticker['Lower Band'] = talib.BBANDS(ticker["close"], timeperiod=21, nbdevup=2, nbdevdn=2, matype=0)

            '''ticker.ta.macd(close='close', fast=13, slow=21, signal=9, append=True)
            ticker.ta.macd(close='close', fast=34, slow=144, signal=9, append=True)
            ticker.ta.stoch(high='high', low='low', k=7, d=3, append=True)'''

            timeToIndex = datetime.now() + timedelta(hours=2) - timedelta(minutes=minutes_to_add)
            delta = timedelta(minutes=minutes_to_add)
            timeToIndex = round_dt(timeToIndex, delta)

            candle = ticker.loc[ticker['time'] == timeToIndex]

            current_high = float(candle["high"])
            current_low = float(candle["low"])
            current_bb_upper = float(candle['Upper Band'])
            current_bb_lower = float(candle['Lower Band'])

            '''fastK = float(candle["STOCHk_7_3_3"])
            fastD = float(candle["STOCHd_7_3_3"])

            fastKCurrent = float(ticker.loc[ticker['time'] == (timeToIndex+timedelta(minutes=minutes_to_add))]["STOCHk_7_3_3"])
            fastDCurrent = float(ticker.loc[ticker['time'] == (timeToIndex+timedelta(minutes=minutes_to_add))]["STOCHd_7_3_3"])

            macd144 = float(candle["MACDh_34_144_9"])
            macd21 = float(candle["MACDh_13_21_9"])'''

            '''if ((macd144 < 0 and macd21 > 0) and (fastK > fastD and fastKCurrent < fastDCurrent) and fastK >= 80) or ((macd144 > 0 and macd21 < 0) and (fastK < fastD and fastKCurrent > fastDCurrent) and fastK <= 20):
                print(str(timeToIndex) + " POTENTIAL MACD CROSS " + str(s.name))
                discord.post(content=(str(timeToIndex) + " POTENTIAL MACD CROSS " + str(s.name)))'''

            if ((current_high > current_bb_upper) and (current_low > current_bb_upper)) or ((current_high < current_bb_lower) and (current_low < current_bb_lower)):
                print(str(timeToIndex) + " Full Candle Outside " + str(s.name))
                discord.post(content=(str(timeToIndex) + " Full Candle Outside " + str(s.name)))
        except Exception as e:
            print(e)


def start_system():
    # INITIALISE CONNECTION TO MT5

    if not mt5.initialize(login=user, password=password, server="FTMO-Demo"):
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    current_time = str(datetime.now() + timedelta(hours=2))
    hours = int(current_time[10:13])
    minutes = int(current_time[14:16])
    seconds = int(current_time[17:19])
    if hours==0 and minutes == 0 and seconds == 0:
        print("1 DAY")
        fifteen_minute_full_candle_check("1d")
    if hours%4==0 and minutes == 0 and seconds == 0:
        print("4 HOUR")
        fifteen_minute_full_candle_check("4h")
    if minutes == 0 and seconds == 0:
        print("1 HOUR")
        fifteen_minute_full_candle_check("1h")
    if minutes%15 == 0 and seconds == 0:
        print("15 MINUTE")
        fifteen_minute_full_candle_check("15m")
    '''if seconds == 0:
        print("1 MINUTE")
        fifteen_minute_full_candle_check("1m")'''
    if (hours%22==0) and seconds < 2:
        print("END OF DAY")


while True:
    start_system()