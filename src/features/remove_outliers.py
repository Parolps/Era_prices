import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import erfc
from sklearn.cluster import KMeans
import plotly.express as px

plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["figure.dpi"] = 100

# from sklearn.neighbors import LocalOutlierFactor
# from sklearn.cluster import DBSCAN

df = pd.read_pickle("../../data/interim/01_houses_processed.pkl")

df["SellPrice"].plot.hist()

df.plot(kind="scatter", x="NetArea", y="SellPrice")
plt.yscale("log")
plt.xscale("log")

scale = StandardScaler()
SellPrice = scale.fit_transform(df["SellPrice"].values.reshape(-1, 1)).ravel()
std = 3
mask = (SellPrice >= std) | (SellPrice <= -std)
outliers = SellPrice[mask]

plt.plot(df["NetArea"], df["SellPrice"], "b.", alpha=0.3)
plt.plot(df["NetArea"][mask], outliers, "r.", linewidth=5)

df["NetArea"][(SellPrice >= std) & (SellPrice <= -std).ravel()]
df["NetArea"].values


# X_train = df[["NetArea", "SellPrice"]]
# model = DBSCAN(eps=150000, min_samples=300)
# model.fit(X_train)
# cluster_labels = model.labels_
# plt.scatter(df["NetArea"], df["SellPrice"], c=cluster_labels, alpha=0.3)
# plt.yscale("log")
# plt.xscale("log")
# pd.Series(cluster_labels).unique()

scale = StandardScaler()
NetArea = scale.fit_transform(df["NetArea"].values.reshape(-1, 1)).ravel()
std = 3
mask = (NetArea >= std) | (NetArea <= -std)
outliers = NetArea[mask]

g = sns.JointGrid(
    x=np.log(df["NetArea"]), y=np.log(df["SellPrice"]), height=5, ratio=3, hue=mask * 1
)
g.plot_joint(sns.scatterplot)
g.plot_marginals(sns.kdeplot)


# Outlier detection using distance from the mean (multivariate dataset)


data = df[["ListingArea", "NetArea", "SellPrice"]]
mean = df[["ListingArea", "NetArea", "SellPrice"]].mean(axis=0)
distances = np.sqrt(np.sum((data - mean) ** 2, axis=1))
threshold = np.percentile(distances, 95)
outliers = data[distances > threshold]

g = sns.JointGrid(x=df["NetArea"], y=df["SellPrice"], height=5, ratio=3)
g.plot_joint(sns.scatterplot)
g.plot_marginals(sns.kdeplot)
g.ax_joint.plot(outliers["NetArea"], outliers["SellPrice"], "r.")

# usar o método chauvenet

plt.plot(df["NetArea"], df["SellPrice"], ".", c="royalblue")


def chauvenet_outliers(df, col):
    mu = df[col].mean()
    sigma = df[col].std()
    n = len(df[col])
    chauv = df[col].apply(lambda x: 1 if n * erfc(abs(x - mu) / sigma) < 1 / 2 else 0)
    return chauv


mask = chauvenet_outliers(df, "SellPrice") == 1

plt.plot(df["NetArea"], df["SellPrice"], ".", c="royalblue")
plt.plot(df["NetArea"][mask], df["SellPrice"][mask], ".", c="red")
plt.yscale("log")
plt.xscale("log")

mask = chauvenet_outliers(df, "NetArea") == 1

plt.plot(df["NetArea"], df["SellPrice"], ".", c="royalblue")
plt.plot(df["NetArea"][mask], df["SellPrice"][mask], ".", c="red")
plt.yscale("log")
plt.xscale("log")

mask = chauvenet_outliers(df, "ListingArea") == 1

plt.plot(df["ListingArea"], df["SellPrice"], ".", c="royalblue")
plt.plot(df["ListingArea"][mask], df["SellPrice"][mask], ".", c="red")
plt.yscale("log")
plt.xscale("log")


def plot_chauvenet(df, col):
    mask = chauvenet_outliers(df, col) == 1
    plt.figure(figsize=(8, 8))
    plt.subplot(221)
    plt.plot(df[col], df["SellPrice"], ".", c="royalblue")
    plt.title(fontsize=10, label=f"{col} Raw")

    plt.subplot(222)
    plt.plot(df[col][mask], df["SellPrice"][mask], ".", c="red")
    plt.title(fontsize=10, label=f"{col} Outliers")

    plt.subplot(223)
    plt.plot(df[col], df["SellPrice"], ".", c="royalblue")
    plt.yscale("log")
    plt.xscale("log")
    plt.title(fontsize=10, label=f"{col} Log Scale")

    plt.subplot(224)
    plt.plot(df[col], df["SellPrice"], ".", c="royalblue")
    plt.plot(df[col][mask], df["SellPrice"][mask], ".", c="red")
    plt.yscale("log")
    plt.xscale("log")
    plt.title(fontsize=10, label=f"{col} Log Scale Outliers")
    plt.show()


plot_chauvenet(df, "NetArea")

df[mask].corr()["SellPrice"].sort_values(ascending=False)

# vou tirar os outliers mais fáceis, os mal colocados.
# ha lats e lngs mal feitas.

df.plot(kind="scatter", x="Lng", y="Lat")

city_median_coords = df.groupby(["City"]).median(numeric_only=True)[["Lng", "Lat"]]
lng_dict = city_median_coords["Lng"].to_dict()
lat_dict = city_median_coords["Lat"].to_dict()

df.loc[df["Lng"] >= -5, "Lng"] = df.loc[df["Lng"] >= -5]["City"].apply(
    lambda x: lng_dict[x]
)
df.loc[df["Lat"] <= 10, "Lat"] = df.loc[df["Lat"] <= 10]["City"].apply(
    lambda x: lat_dict[x]
)

# mapa p confirmar outliers
px.scatter_mapbox(
    df, lat="Lat", lon="Lng", mapbox_style="open-street-map", color="City"
)


df.loc[(df["Lng"] >= -25) & (df["Lng"] <= -20), "Lng"] = df.loc[
    (df["Lng"] >= -25) & (df["Lng"] <= -20)
]["City"].apply(lambda x: lng_dict[x])
df.loc[(df["Lat"] <= 36) & (df["Lng"] >= 34), "Lat"] = df.loc[
    (df["Lat"] <= 36) & (df["Lng"] >= 34)
]["City"].apply(lambda x: lat_dict[x])


df.to_pickle("../../data/interim/02_houses_coordsfix.pkl")
