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


df.columns
df.head()
df.info()

feats = [
    "BelongsToDevelopment",
    "BusinessStatus",
    "BusinessType",
    "Ce",
    "Elevator",
    "HasExactLocation",
    "IsDevelopment",
    "Lat",
    "Lng",
    "ListingArea",
    "Localization",
    "NetArea",
    "Parking",
    "PropertyType",
    "Rooms",
    "Wcs",
    "ConstructionFeasibility",
    "City",
    "SellPrice",
]

houses = df[feats].copy()


# fig, ax = plt.subplots()
# labels = df.groupby(["PropertyType"])["SellPrice"].size()[
#     df.groupby(["PropertyType"])["SellPrice"].mean().sort_values().index
# ]

# bars = ax.bar(
#     df.groupby(["PropertyType"])["SellPrice"].mean().sort_values().index,
#     df.groupby(["PropertyType"])["SellPrice"].mean().sort_values(),
# )
# ax.bar_label(bars, fmt="{:.2E}", rotation=45, labels=labels)
# ax.set_title("Property Type mean value and respective counts")
# ax.set_xticklabels(
#     rotation=90,
#     labels=df.groupby(["PropertyType"])["SellPrice"].mean().sort_values().index,
# )
# ax.set_ylabel("Sell Price")
# plt.show()

houses.info()


def convert_bool_to_int(df):
    # Identify boolean columns
    bool_columns = df.select_dtypes(include="bool").columns

    # Convert boolean values to integers (1 and 0)
    df[bool_columns] = df[bool_columns] * 1

    return df


houses = convert_bool_to_int(houses)

houses[houses["Lat"].isna()][["Lat", "Lng"]].to_dict()

houses["Lng"] = houses["Lng"].fillna(houses.groupby(["City"])["Lng"].median())
houses["Lat"] = houses["Lat"].fillna(houses.groupby(["City"])["Lat"].median())

houses.groupby(["City"])["Lat"].median().to_dict()

houses.info()

houses.groupby(["City"])[["Lat", "Lng"]].median()
