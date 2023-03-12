import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import matplotlib.dates as mpl_dates
from creds import user, password
from support_resistance_swing import support_res_print

if not mt5.initialize(login=user, password=password, server="FTMO-Demo"):
    print("initialize() failed, error code =", mt5.last_error())
    quit()

symbols = mt5.symbols_get()
sup_res_array_1W = []
sup_res_array_1D = []
symbols_xx = []

for s in symbols:
    if s.name != "XRPUSD":
        support_1W = str(support_res_print(s.name, "1W")).replace("[","{")
        support_1W = support_1W.replace("]","}")

        support_1D = str(support_res_print(s.name, "1D")).replace("[","{")
        support_1D = support_1D.replace("]", "}")

        sup_res_array_1W.append(support_1W)
        sup_res_array_1D.append(support_1D)

        symbols_xx.append(s.name)

        print(s.name, support_1W, support_1D)


def replaceSR(mystring, tf):
    start = mystring.find("{")
    end = mystring.find("}")

    if start != -1 and end != -1:
        result1 = mystring[0:start+1]
        result2 = mystring[end:-1]

        if tf == "1W":
            SR = sup_res_array_1W
            SR_LIST = ",".join([str(i) for i in SR])
            new_line = (result1+SR_LIST+result2)


        if tf == "1D":
            SR = sup_res_array_1D
            SR_LIST = ",".join([str(i) for i in SR])
            new_line = (result1+SR_LIST+result2)

        return (new_line)

save_string = ""
remove_whitespace = ""

file_loc = "C:/Users/nikit/AppData/Roaming/MetaQuotes/Terminal/49CDDEAA95A409ED22BD2287BB67CB9C/MQL5/Experts/Support_Resistance_Multi.mq5"

with open(file_loc,"r") as f:
    for i in f.readlines():
        if not i.strip():
            continue
        if i:
            remove_whitespace = (remove_whitespace+i+"\n")
f.close()

f = open(file_loc,"w+")
f.writelines(remove_whitespace)
f.close()

with open(file_loc, "r", encoding="cp1252") as f:
    for line in f:
        if "Supports1W[120][50]" in line:
            replace = replaceSR(line, "1W")
            save_string = (save_string+replace+"\n")
        elif "Supports1D[120][100]" in line:
            replace = replaceSR(line, "1D")
            save_string = (save_string+replace+"\n")
        else:
            save_string = (save_string+line+"\n")

f.close()

f = open(file_loc,"w+")
f.writelines(save_string)
f.close()

print(symbols_xx)