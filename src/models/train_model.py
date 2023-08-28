import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import Lasso, Ridge, LinearRegression, ElasticNet
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor

plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["figure.dpi"] = 100

df = pd.read_pickle("../../data/interim/03_houses_withfeats.pkl")


df.head()
df.info()

y = df["SellPrice"]
y_log = df["log_SellPrice"]
X = df.drop(labels=["SellPrice", "log_SellPrice"], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y_log, test_size=0.2)

# Quick check feature importances
# Nota!!! - aqui tratou-se Wcs e Rooms como numeric ao invés de categoria

num_cols = X_train.select_dtypes(np.number).columns.values
object_cols = X_train.select_dtypes(object).columns.values


preprocessing = ColumnTransformer(
    [
        ("num_transf", StandardScaler(), num_cols),
        ("cat_transf", OneHotEncoder(handle_unknown="ignore"), object_cols),
    ],
    verbose_feature_names_out=True,
)

rf = make_pipeline(preprocessing, RandomForestRegressor())
rf.fit(X_train, y_train)

rf_importances = pd.DataFrame(
    {"Importances": rf.steps[1][1].feature_importances_},
    index=preprocessing.get_feature_names_out(),
)

rf_importances.sort_values(["Importances"], ascending=False).head(10).plot.barh()


# Primeiro test drive com CV
# Random Forest
rf_rmses = -cross_val_score(
    rf, X_train, y_train, cv=5, scoring="neg_root_mean_squared_error"
)  # 0.41 rmse mas pode ser random luck

GridSearchCV()  #!!!

# Modelos a utilizar
# -Linear Model
# -Lasso (feature selection)
# -Ridge
# ElasticNet
# SVM regressor
# RandomForest
#   - se overfittar - bootstrap - bagging ou pasting
# KNeighbors

# !! Aplicar Polynomial Features tb

# K_reg = KNeighborsRegressor(n_neighbors=20)
# K_reg.fit(X_train, y_test)

lr = LinearRegression()
Lasso_reg = Lasso()
Ridge_reg = Ridge()
knr = KNeighborsRegressor()
rf = RandomForestRegressor()

model_list = [lr, Lasso_reg, Ridge_reg, knr, rf]
model_results = []

for model in model_list:
    pipe = make_pipeline(preprocessing, model)
    pipe.fit(X_train, y_train)
    model_results.append(pipe)

scores = []
for model in model_results:
    score = model.score(X_train, y_train)
    scores.append(score)

model_results[1].score(X_test, y_test)
model_results[0].steps[-1][0]

pd.Series(
    scores, index=[model.steps[-1][0] for model in model_results]
).sort_values().plot.barh()

pd.Series(scores, index=[model.steps[-1][0] for model in model_results]).sort_values()
model_results[-1].score(X_test, y_test)
# O modelo RandomForestRegressor tinha coeficiente de determinação de 0.96 no set de treino mas com o set de test teve apenas 0.77
# overfit
# mudar o bootstrapzzz

fit_score = []

for model in model_results:
    fit_score.append(model.score(X_test, y_test))

pd.Series(
    fit_score, index=[model.steps[-1][0] for model in model_results]
).sort_values()

# Posso sempre tentar mais modelos, ou grid search no melhor
# se fizer ensemble destes modelos todos talvez saia melhor tb

ada = AdaBoostRegressor(
    DecisionTreeRegressor(max_depth=10),
    n_estimators=500,
)

pipe = make_pipeline(preprocessing, ada)
pipe.fit(X_train, y_train)

pipe.score(X_train, y_train)
pipe.score(X_test, y_test)

plt.plot(X_train["log_NetArea"], y_train, "b.", label="Train")
plt.plot(X_train["log_NetArea"], pipe.predict(X_train), "r.", label="Test")
plt.legend()

plt.plot(X_test["log_NetArea"], y_test, "b.", label="Train")
plt.plot(X_test["log_NetArea"], pipe.predict(X_test), "r.", label="Test")
plt.legend()

mean_squared_error(y_train, pipe.predict(X_train))
mean_squared_error(y_test, pipe.predict(X_test))

# modelo AdaBoost
np.sqrt(mean_squared_error(y_test, pipe.predict(X_test)))

# modelo RandomForest
np.sqrt(mean_squared_error(y_test, model_results[-1].predict(X_test)))
