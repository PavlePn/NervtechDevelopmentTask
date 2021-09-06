from typing import Any, List
from numpy.core.records import array
from numpy.ma import sqrt
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame

# Auxiliary funcions


def prepare_data(df: DataFrame):
    df_ret = pd.DataFrame(
        columns=["dtime", "time_dif", "velocity", "acceleration", "jerk"])
    df_diff = df.diff()
    df_ret["time_dif"] = df_diff["timestamp"] / 1000.
    df_ret["dtime"] = (df["timestamp"]-df["timestamp"][0]) / \
        1000  # delta t in [s]
    df_ret["velocity"] = np.sqrt(df["x_velocity"]**2+df["y_velocity"]**2)
    df_ret["acceleration"] = np.gradient(
        df_ret["velocity"], df_ret["dtime"], edge_order=2)
    # smoothing acc profile so numerical derivative of jerk can be obtained
    filt_acc = df_ret["acceleration"].rolling(16).mean()
    df_ret["jerk"] = np.gradient(
        filt_acc, df_ret["dtime"], edge_order=2)
    return df_ret


# DATA READ AND PREPROCESING
col_list = ["timestamp", "x_position",
            "y_position", "x_velocity", "y_velocity"]

df_av = pd.read_csv('AV/medical_data-scenario1.csv',
                    usecols=col_list, delimiter=";")
df_dn = pd.read_csv('DN/medical_data-scenario1.csv',
                    usecols=col_list, delimiter=";")
df_js = pd.read_csv('JS/medical_data-scenario1.csv',
                    usecols=col_list, delimiter=";")
df_mb = pd.read_csv('MB/medical_data-scenario1.csv',
                    usecols=col_list, delimiter=";")
df_sm = pd.read_csv('SM/medical_data-scenario1.csv',
                    usecols=col_list, delimiter=";")

dfs = [df_av, df_dn, df_js, df_mb, df_sm]
names = ["AV", "DN", "JS", "MB", "SM"]

# JERK CALCULATION
results = []

for i, df in enumerate(dfs):
    dfr = prepare_data(df)
    results.append(dfr)
    #print((dfr.loc[dfr["jerk"] > 0.9, "jerk"].count()))


#  DEFINITION OF RESULTS INTO CLASSES

# Class definition similar to paper
stdevJ = []
meanJ = []
ratioJ = []
window = 256

for i, r in enumerate(results):
    t = r.dropna()
    cur_ratio = []
    start = 50
    end = start + window
    while end < len(t):
        s = np.std((t["jerk"][start:end]))
        m = np.mean(abs(t["jerk"]))
        stdevJ.append(s)
        meanJ.append(m)
        cur_ratio.append(s/m)
        start = end + 1
        end += window
        end = min(end, len(t))
    ratioJ.append(cur_ratio)
score = []
for r in ratioJ:
    l = len(r)
    s = 0
    for i in range(l):
        if r[i] > 2:
            s += 0
        if r[i] > 1 and r[i] <= 2:
            s += 1
        if r[i] > 0.5 and r[i] <= 1:
            s += 2
        if r[i] > 0.1 and r[i] <= 0.5:
            s += 3
        if r[i] > 0.01 and r[i] <= 0.1:
            s += 4
        if r[i] <= 0.01:
            s += 5
    score.append(np.ceil(s/l))
dfC = pd.DataFrame(columns=["name", "class"])
dfC["class"] = score
dfC["name"] = names
print("Definition of class by rule")
print(dfC)
print("Legend: 1 - very agressive; 2 - agressive; 3 - normal; 4 - calm; 5 - very calm")
print("\n\n\n")


# absolute scoring
percent = []
safe = 0.9
for i, r in enumerate(results):
    p = r.loc[r["jerk"] > safe, "time_dif"].sum()
    p = p / r["dtime"].iloc[-1] * 100.
    percent.append(p)
print("Ranging between drivers on safty driving")
dfC["class"] = percent
dfC = dfC.sort_values("class", ascending=True).reset_index(drop=True).rename(columns={"class" : "unsafe drive time [%]"})
print(dfC)

