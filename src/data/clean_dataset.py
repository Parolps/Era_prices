import pandas as pd


def clean_dataframe(df, threshold):
    # Calculate the number of missing values for each column
    missing_values = df.isnull().sum()

    # Filter columns with less than 10000 missing values
    columns_to_keep = missing_values[missing_values < threshold].index

    # Create a new DataFrame with the selected columns
    cleaned_df = df[columns_to_keep]

    return cleaned_df


def clear_cols(df):

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

    df["Wcs"] = (
        df["Wcs"]
        .apply(lambda x: x.split("-")[1] if "-" in str(x) else x)
        .astype("float64")
    )

    return df


def main():

    threshold = 5_000
    df = pd.read_csv("../../data/raw/raw_houses.csv", usecols=cols)
    print(f"Getting rid of cools with more that {threshold} nulls")
    df = clean_dataframe(df, threshold)

    # fixing columns and datatypes
    df = clear_cols(df)

    print("\nSaving dataframe:\n")
    print(df.info())
    return df.to_csv("../../data/interim/houses.csv")


if __name__ == "__main__":

    cols = [
        "Title",
        "Parking",
        "Ce",
        "Elevator",
        "Lat",
        "Lng",
        "ListingArea",
        "Localization",
        "NetArea",
        "Parking",
        "PropertyType",
        "Rooms",
        "Wcs",
        "SellPrice",
    ]

    main()
