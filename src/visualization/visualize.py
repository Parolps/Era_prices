import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import rbf_kernel
import geopandas as gp
import contextily as ctx
from sklearn.preprocessing import MinMaxScaler

plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["figure.dpi"] = 100


df = pd.read_pickle("../../data/interim/01_houses_processed.pkl")


df.head()
df.info()


df.corr(numeric_only=True)["SellPrice"]


fig, ax = plt.subplots(figsize=(12, 5))
labels = df.groupby(["PropertyType"])["SellPrice"].size()[
    df.groupby(["PropertyType"])["SellPrice"].mean().sort_values().index
]

bars = ax.bar(
    df.groupby(["PropertyType"])["SellPrice"].mean().sort_values().index,
    df.groupby(["PropertyType"])["SellPrice"].mean().sort_values(),
)
ax.bar_label(bars, fmt="{:.2E}", rotation=45, labels=labels)
ax.set_title("Property Type mean value and respective counts")
ax.set_xticklabels(
    rotation=90,
    labels=df.groupby(["PropertyType"])["SellPrice"].mean().sort_values().index,
)
ax.set_ylabel("Sell Price")
plt.savefig("../../reports/figures/Property_type_SellPrice.png", bbox_inches="tight")
plt.show()


sns.heatmap(
    df.corr(numeric_only=True), mask=np.triu(df.corr(numeric_only=True)), annot=True
)

# Vê-se alguma colinearidade entre as variávceis rooms netarea parking wcs

# Vamos ver a skewness das variáveis

num_cols = df.select_dtypes(np.number).columns

# fig, ax = plt.subplots(figsize=(20, 20))
sns.pairplot(df[num_cols], kind="scatter")
plt.show()

# Não há assim mt linearidade dos dados até agr

object_cols = df.select_dtypes(object).columns

df["Ce"].value_counts().plot.bar()
df["PropertyType"].value_counts().plot.bar()

sns.scatterplot(df, x="Wcs", y="Rooms", hue=np.log(df["SellPrice"]))


# Tenho que melhorar
df["SellPrice"].plot.box()


# LOLLIPOP SPREAD

df_ordered = df.sort_values(["City", "SellPrice"])

plt.stem(
    df_ordered.groupby(["City"])
    .median(numeric_only=True)["SellPrice"]
    .sort_values()
    .tail(20)
)
plt.xticks(
    ticks=range(0, 20),
    labels=df_ordered.groupby(["City"])
    .median(numeric_only=True)["SellPrice"]
    .sort_values()
    .tail(20)
    .index,
    rotation=45,
)


def lollipop_horizontal(df_ordered, target, n, head):
    if head:
        maxs = df_ordered.groupby(["City"]).max().sort_values([target])[target].head(n)
        index = (
            df_ordered.groupby(["City"])
            .max()
            .sort_values([target])[target]
            .head(n)
            .index
        )
        mins = df_ordered.groupby(["City"])[target].min()
        mins = mins[index]

        plt.hlines(xmax=maxs, xmin=mins, y=range(0, n), color="grey", alpha=0.4)
        plt.scatter(maxs, range(0, n), color="skyblue", label="Max")
        plt.scatter(mins, range(0, n), color="green", label="Min")
        plt.yticks(range(0, n), index)
        plt.xlabel("Spread")
        plt.legend(loc="lower right")

    else:
        maxs = df_ordered.groupby(["City"]).max().sort_values([target])[target].tail(n)
        index = (
            df_ordered.groupby(["City"])
            .max()
            .sort_values([target])[target]
            .tail(n)
            .index
        )
        mins = df_ordered.groupby(["City"])[target].min()
        mins = mins[index]

        plt.hlines(xmax=maxs, xmin=mins, y=range(0, n), color="grey", alpha=0.4)
        plt.scatter(maxs, range(0, n), color="skyblue", label="Max")
        plt.scatter(mins, range(0, n), color="green", label="Min")
        plt.yticks(range(0, n), index)
        plt.xlabel("Spread")
        plt.legend(loc="lower right")


lollipop_horizontal(df_ordered, "SellPrice", 30, head=False)
plt.savefig("../../reports/figures/Lollipop_spread_city.png", bbox_inches="tight")


# boxplot das 20 zonas com maior sellprice pela mediana

index = (
    df.groupby(["City"])
    .median(numeric_only=True)
    .sort_values(["SellPrice"], ascending=False)
    .head(20)
    .index
)

df.groupby(["City"]).size().loc[index]
df.loc[df["City"].isin(index)]

sns.boxplot(df.loc[df["City"].isin(index)], x="SellPrice", y="City")

# Há muitas cidades com poucas instâncias portanto medianas tortas

index = df.groupby("City").size().sort_values(ascending=False).head(20).index

sns.boxplot(df.loc[df["City"].isin(index)], x="SellPrice", y="City")

index = (
    df.loc[df["City"].isin(index)]
    .groupby(["City"])
    .median()
    .sort_values(["SellPrice"], ascending=False)
    .index
)


sns.boxplot(
    df.set_index(["City"]).loc[index].reset_index(),
    x="SellPrice",
    y="City",
    palette="dark:salmon_r",
)
plt.title("Top 20 Cities")
plt.xlabel("Price")
plt.ylabel("Cities")
plt.savefig("../../reports/figures/Top20_Cities_Price_Boxplot.png", bbox_inches="tight")

# gráfico lat lng com cluster similarity
# map portugal


class ClusterSimilarity(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=10, gamma=1.0, random_state=None):
        self.n_clusters = n_clusters
        self.gamma = gamma
        self.random_state = random_state

    def fit(self, X, y=None, sample_weight=None):
        self.kmeans_ = KMeans(self.n_clusters, random_state=self.random_state)
        self.kmeans_.fit(X, sample_weight=sample_weight)
        return self  # Retornar self sempre !!!

    def transform(self, X):
        return rbf_kernel(X, self.kmeans_.cluster_centers_, gamma=self.gamma)

    def get_features_names_out(self, names=None):
        return [f"Cluster {i} similarity" for i in range(self.n_clusters)]


cluster_simil = ClusterSimilarity(n_clusters=10, gamma=1, random_state=42)
similarities = cluster_simil.fit_transform(
    df[["Lat", "Lng"]], sample_weight=df["SellPrice"]
)

df["Max cluster similarity"] = similarities.max(axis=1)


continent = df.query("Lng >= -10 & Lng <= -6")
cond_bool = np.where(
    (cluster_simil.kmeans_.cluster_centers_[:, 1] >= -10)
    & (cluster_simil.kmeans_.cluster_centers_[:, 1] <= -6)
)
continent_clusters = cluster_simil.kmeans_.cluster_centers_[cond_bool]

ax = continent.plot(
    kind="scatter",
    x="Lng",
    y="Lat",
    grid=True,
    #    label="Preço",
    c="Max cluster similarity",
    cmap="jet",
    colorbar=True,
    legend=True,
    sharex=False,
    figsize=(10, 7),
)
ax.plot(
    continent_clusters[:, 1],
    continent_clusters[:, 0],
    linestyle="",
    color="black",
    marker="X",
    markersize=8,
    label="Cluster centers",
)
ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.OpenStreetMap.Mapnik)
ax.axis([-10, -6, 36.8, 42.5])
ax.legend(loc="upper right", fontsize="12")
plt.savefig("../../reports/figures/Continent_map_clusters.png", bbox_inches="tight")


# df.plot(
#     kind="scatter",
#     x="Lng",
#     y="Lat",
#     grid=True,
#     label="Preço",
#     c="Max cluster similarity",
#     cmap="jet",
#     colorbar=True,
#     legend=True,
#     sharex=False,
#     figsize=(10, 7),
# )
# plt.plot(
#     cluster_simil.kmeans_.cluster_centers_[:, 1],
#     cluster_simil.kmeans_.cluster_centers_[:, 0],
#     linestyle="",
#     color="black",
#     marker="X",
#     markersize=20,
#     label="Cluster centers",
# )
# plt.axis([-10, -5, 36, 43])

# df["SellPrice"].plot.bar()
# df.head()

# MIN_MAX
# X_std = (continent["SellPrice"] - continent["SellPrice"].min(axis=0)) / (
#     continent["SellPrice"].max(axis=0) - continent["SellPrice"].min(axis=0)
# )
# sizes = X_std * (7 - 3) + 3
