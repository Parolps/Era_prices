import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import rbf_kernel
import numpy as np


plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["figure.dpi"] = 100

df = pd.read_pickle("../../data/interim/01_houses_processed.pkl")

df.head()
df.info()

# Tenho que encodar as categorias


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
    np.sqrt(df["Lat"] ** 2 + df["Lng"] ** 2),
    "r.",
)
np.sqrt(df["Lat"] ** 2 + df["Lng"] ** 2)
