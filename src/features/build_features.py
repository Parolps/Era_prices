import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.decomposition import PCA
import numpy as np
import plotly.express as px

plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["figure.dpi"] = 100

df = pd.read_pickle("../../data/interim/02_houses_coordsfix.pkl")

df.head()
df.info()

# Fazer cluster similarity:
# Código proveniente de: Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow
# O TransformerMixin dá-nos o método fit_transform logo
# Base estimator sem *args e **kwargs dá-nos get_params() e set_params()


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

df["Max Cluster Similarity"] = similarities.max(axis=1)

df.plot(kind="scatter", x="Max Cluster Similarity", y="SellPrice")

df["Max Cluster Similarity"].hist()

plt.plot(
    df["Max Cluster Similarity"],
    np.log(df["Lat"] ** 2 + df["Lng"] ** 2),
    "r.",
)


log_df = pd.DataFrame(
    {
        "log_NetArea": np.log(df["NetArea"]),
        "log_SellPrice": np.log(df["SellPrice"]),
        "log_ListingArea": np.log(df["ListingArea"]),
    }
)

pca = PCA(3)

log_df_pca = pd.DataFrame(
    pca.fit_transform(log_df), columns=["pca_1", "pca_2", "pca_3"]
)


fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(projection="3d")
ax.scatter(
    log_df_pca.iloc[:, 0], log_df_pca.iloc[:, 1], log_df_pca.iloc[:, 2], alpha=0.4
)
ax.view_init(0, 40)


fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(projection="3d")
ax.scatter(log_df.iloc[:, 0], log_df.iloc[:, 1], log_df.iloc[:, 2])
ax.view_init(10, 60)


fig = px.scatter_3d(log_df, "log_NetArea", "log_SellPrice", "log_ListingArea")
fig.show()


fig = px.scatter_3d(log_df_pca, "pca_1", "pca_2", "pca_3")
fig.show()

pca.explained_variance_.sum()
pca.explained_variance_ratio_[:2].sum()

## A listing area e net area são colineares mas relacionam-se bem com o sellprice
## Construindo as features
## - log areas

df.info()

to_log = ["NetArea", "ListingArea", "SellPrice"]

for col in to_log:
    df["log_" + col] = np.log(df[col])


## secalhar podia pôr umas feats squared

to_square = to_log + ["Parking", "Rooms", "Wcs", "Elevator"]

for col in to_square:
    df["square_" + col] = df[col] ** 2

df.head()

df.plot(kind="scatter", x="NetArea", y="square_NetArea")

sns.heatmap(df.corr(numeric_only=True))

bar = df.corr(numeric_only=True)["log_SellPrice"].sort_values().plot.bar()

df.to_pickle("../../data/interim/03_houses_withfeats.pkl")
