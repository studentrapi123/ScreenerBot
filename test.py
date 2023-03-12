import MetaTrader5 as mt5
from creds import *

if not mt5.initialize(login=user, password=password, server="FTMO-Demo"):
    print("initialize() failed, error code =", mt5.last_error())
    quit()

positions=mt5.positions_get()

if len(positions)>0:
    print("Total positions on USDCHF =",len(positions))
    # display all open positions
    for position in positions:
        print(position)