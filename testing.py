from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import talib
from support_resistance_swing import support_res_return_swing
from support import support_res_return_scalp
import time
from creds import user, password
from discordwebhook import Discord
from colorama import Fore

def support_resistance_strat():
    symbols = mt5.symbols_get()

    for s in symbols:
        symbol_spread = int((mt5.symbol_info(s.name)).spread)
        if s.name != "USDHKD" and s.name != "BAYGn" and symbol_spread < 15 and s.name != "T":
            try:
                percent_change_swing = support_res_return_swing(s.name, "1D")
                percent_change2_swing = support_res_return_swing(s.name, "1W")
            except:
                print(s.name)

            if (percent_change_swing[0] < 0.005 and percent_change_swing[0] > -0.005) or (percent_change2_swing[0] < 0.005 and percent_change2_swing[0] > -0.005):
                print(Fore.GREEN+"[SWING] NEXT TO SUPPORT OR RESISTANCE " + str(s.name)+ " "+str(percent_change_swing[0])+" "+str(percent_change_swing[1]))
                discord = Discord(url="https://discordapp.com/api/webhooks/1029427336128507987/5TIfYfDoDgCwcR_vOJg7X0E3VyQk_dFD3lF3Vv9_2BYSNbEPhluoMPNZj_eDAM7sJeTP")
                discord.post(content=(("[SWING] NEXT TO SUPPORT OR RESISTANCE " + str(s.name)+ " "+str(percent_change_swing[0])+" "+str(percent_change_swing[1]))))

            try:
                percent_change_scalp = support_res_return_scalp(s.name, "1D")
                percent_change2_scalp = support_res_return_scalp(s.name, "4H")
            except:
                print(s.name)

            if (percent_change_scalp[0] < 0.005 and percent_change_scalp[0] > -0.005) or (percent_change2_scalp[0] < 0.005 and percent_change2_scalp[0] > -0.005):
                print(Fore.BLUE+"[SCALP] NEXT TO SUPPORT OR RESISTANCE " + str(s.name)+ " "+str(percent_change_swing[0])+" "+str(percent_change_swing[1]))
                discord = Discord(url="https://discordapp.com/api/webhooks/1030040818351874058/yIYcStukzW8tt_-VagopcQo2R6cbMWYY9nV-1nAoiPCP38aV7SIwL6qChegjsGI9w1x6")
                discord.post(content=(("[SCALP] NEXT TO SUPPORT OR RESISTANCE " + str(s.name)+ " "+str(percent_change_swing[0])+" "+str(percent_change_swing[1]))))


            rates = mt5.copy_rates_from_pos(str(s.name), mt5.TIMEFRAME_M15, 0, 100)

            ticker = pd.DataFrame(rates)
            ticker['time'] = pd.to_datetime(ticker['time'], unit='s')

            close = float(ticker['close'].take([-1]))

            ticker['Upper Band'], ticker['Middle Band'], ticker['Lower Band'] = talib.BBANDS(ticker["close"],timeperiod=21, nbdevup=2,nbdevdn=2, matype=0)
            bb_upper = float(ticker['Upper Band'].take([-1]))
            bb_lower = float(ticker['Lower Band'].take([-1]))

            bb_lower_percent = ((bb_lower - close) / close) * 100
            bb_upper_percent = ((close - bb_upper) / bb_upper) * 100

            if bb_lower_percent > 0.3 or bb_upper_percent > 0.3:
                print(Fore.RED+str(ticker['time'].iloc[-2]) + " OVEREXTENSION " + str(s.name))
                discord = Discord(url="https://discordapp.com/api/webhooks/1029428019732959282/Th2JE7DOzt3SzJlm-XOZfvXoWf6qx2GzjMiuwVLPGs1i9OpUtOnXMyPoQjereGYlSTRl")
                discord.post(content=(str(ticker['time'].iloc[-2]) + " OVEREXTENSION " + str(s.name)))


def start_system():
    # INITIALISE CONNECTION TO MT5

    if not mt5.initialize(login=user, password=password, server="Eightcap-Demo"):
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    current_time = str(datetime.now())
    hours = int(current_time[10:13])
    minutes = int(current_time[14:16])
    seconds = int(current_time[17:19])

    if seconds < 55:
        support_resistance_strat()


while True:
    start_system()



'''def end_of_day():
    symbols = mt5.symbols_get(group="*,!GOOG, !FB, !NFLX, !NVDA, !META, !VOWG_p, !DBKGn, !LVMH, !MSFT, !BABA, !BAC, !ALVG, !AAPL, !WMT, !V, !BAYGn, !IBE, !ERBN.f, !AMZN, !TSLA, !ZM")
    time.sleep(1)

    for s in symbols:
        rates = mt5.copy_rates_from_pos(str(s.name), mt5.TIMEFRAME_M15, 0, 100)
        discord = Discord(url="https://discordapp.com/api/webhooks/1034934795941199882/ZlL6Jvcy4w092NYMVSNBVrL-VQnWO0QwKFWWzLE-h7bdo30ML_CWTJsFb4tVljOTO2yu")

        ticker = pd.DataFrame(rates)
        ticker['time'] = pd.to_datetime(ticker['time'], unit='s')

        ticker['10 MA'] = ticker["close"].rolling(window=10).mean()
        ticker['5 MA'] = ticker["close"].rolling(window=5).mean()

        ticker_recent = ticker.tail(1)
        ticker_previous = (ticker.tail(2)).head(1)

        ticker_recent_10 = ticker_recent["10 MA"].values
        ticker_recent_5 = ticker_recent["5 MA"].values

        ticker_previous_10 = ticker_previous["10 MA"].values
        ticker_previous_5 = ticker_previous["5 MA"].values

        print(ticker_previous_10, ticker_previous_5, ticker_recent_5, ticker_recent_10, s.name)

        if ticker_recent_5 > ticker_recent_10 and ticker_recent_5 < ticker_recent_10:
            print("SHORT "+s.name)

        if ticker_previous_5 > ticker_previous_10 and ticker_previous_5 < ticker_previous_10:
            print("LONG " + s.name)

end_of_day()'''