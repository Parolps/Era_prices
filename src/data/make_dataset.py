import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["figure.dpi"] = 100

pd.options.display.max_columns = 9999

df = pd.read_csv("../../data/raw/Homes_raw.csv", index_col=[0]).reset_index(drop=True)


def clean_dataframe(df, threshold):
    # Calculate the number of missing values for each column
    missing_values = df.isnull().sum()

    # Filter columns with less than 10000 missing values
    columns_to_keep = missing_values[missing_values < threshold].index

    # Create a new DataFrame with the selected columns
    cleaned_df = df[columns_to_keep]

    return cleaned_df


df = clean_dataframe(df, 10_000)

# Limpar as features todas dos dados Raw

df["SellPrice"] = df["SellPrice"].apply(
    lambda x: x.split(",")[1]
    .replace("€", "")
    .replace(".", "")
    .split(":")[1]
    .strip()
    .replace("'", "")
)

to_drop = df[df["SellPrice"] == "Sob Consulta"]
df.drop(to_drop.index, axis=0, inplace=True)
df["SellPrice"] = df["SellPrice"].astype("float64")


df["BusinessStatus"] = df["BusinessStatus"].apply(
    lambda x: x.split(":")[2].replace("'", "").replace("}", "").strip()
    if type(x) == str
    else x
)

df["ListingArea"] = (
    df["ListingArea"]
    .apply(lambda x: x.split("-")[1] if "-" in str(x) else x)
    .astype("float64")
)

df["NetArea"] = (
    df["NetArea"]
    .apply(lambda x: x.split("-")[1] if "-" in str(x) else x)
    .astype("float64")
)

df["Rooms"] = (
    df["Rooms"]
    .apply(lambda x: x.split("-")[1] if "-" in str(x) else x)
    .astype("float64")
)

df["Rooms"] = df["Rooms"].apply(lambda x: 1 if x == 0 else x)

df["RealEstate"] = df["RealEstate"].apply(
    lambda x: str(x).split("'")[11].split("ERA ")[1] if ":" in str(x) else x
)


df["Lng"] = (
    df["Lng"]
    .apply(lambda x: x.replace(",", ".") if "," in str(x) else x)
    .astype("float64")
)

df["Lat"] = (
    df["Lat"]
    .apply(lambda x: x.replace(",", ".") if "," in str(x) else x)
    .astype("float64")
)

df["City"] = df["Localization"].apply(lambda x: x.split(",")[-1].strip())

df["Parking"] = (
    df["Parking"]
    .apply(lambda x: x.split("-")[1] if "-" in str(x) else x)
    .astype("float64")
)

df["Wcs"] = (
    df["Wcs"].apply(lambda x: x.split("-")[1] if "-" in str(x) else x).astype("float64")
)


df.columns
df.head()


feats = [
    "Ce",
    "Elevator",
    "HasExactLocation",
    "Lat",
    "Lng",
    "ListingArea",
    "Localization",
    "NetArea",
    "Parking",
    "PropertyType",
    "Rooms",
    "Wcs",
    "City",
    "SellPrice",
]

houses = df[feats].copy()


def convert_bool_to_int(df):
    # Identify boolean columns
    bool_columns = df.select_dtypes(include="bool").columns

    # Convert boolean values to integers (1 and 0)
    df[bool_columns] = df[bool_columns] * 1

    return df


houses = convert_bool_to_int(houses)


## Imputar as features

houses["Ce"] = houses["Ce"].fillna(houses["Ce"].mode().values[0])

# Imputar a lat e lng com base nas medianas de cada cidade
for col in ["Lat", "Lng"]:
    dict_col = houses.groupby(["City"]).median(numeric_only=True)[[col]].to_dict()[col]
    houses[col] = houses[col].fillna(houses["City"].map(dict_col))

#  há 3 cidade que so aparecem uma vez e sem valores, portanto não temos mediana possivel vamos dropar

houses.dropna(subset=["Lat", "Lng"], inplace=True)


houses[houses["ListingArea"].isna() | houses["NetArea"].isna()][
    ["ListingArea", "NetArea"]
]

# vou tentar ver a percentagem média de diferença entre a listing area e a net area

(houses["NetArea"] / (houses["ListingArea"] + houses["NetArea"])).mean()

# Percentagem de aproveitamento do terreno
(houses["NetArea"] / (houses["ListingArea"] + houses["NetArea"])).plot.hist()
plt.axvline(
    (houses["NetArea"] / (houses["ListingArea"] + houses["NetArea"])).mean(),
    linestyle="--",
    c="red",
    label="Mean",
)
plt.axvline(
    (houses["NetArea"] / (houses["ListingArea"] + houses["NetArea"])).median(),
    linestyle="--",
    c="purple",
    label="Median",
)
plt.legend()

# -- ronda os 0.46 porcento portanto vamos imputar com base nisto
# -- introduzi algum viés mas wtv

houses[houses["ListingArea"].isna() | houses["NetArea"].isna()][
    ["ListingArea", "NetArea"]
]

houses.loc[houses["NetArea"].isna(), "NetArea"] = houses["ListingArea"] * 0.46
houses.loc[houses["ListingArea"].isna(), "ListingArea"] = houses["NetArea"] / 0.46

houses.loc[houses["ListingArea"].isna()]

houses["ListingArea"] = houses["ListingArea"].fillna(houses["ListingArea"].median())
houses.loc[houses["NetArea"].isna(), "NetArea"] = houses["ListingArea"] * 0.46


houses["Parking"] = houses["Parking"].fillna(houses["Parking"].median())

houses["Rooms"].plot.hist()

houses[houses["Rooms"].isna()]
houses["Rooms"] = houses["Rooms"].fillna(houses["Rooms"].median())

houses["Wcs"] = houses["Wcs"].fillna(houses["Wcs"].median())

houses.to_pickle("../../data/interim/01_houses_processed.pkl")

houses.info()
