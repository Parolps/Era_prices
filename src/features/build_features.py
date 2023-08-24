import pandas as pd
import matplotlib.pyplot as plt


plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["figure.dpi"] = 100

df = pd.read_pickle("../../data/interim/01_houses_processed.pkl")

df.head()
df.info()

# Fazer cluster similarity
