
# ==========================================
# preprocess.py
#
# Dataset Preprocessing
#
# Thesis:
# Chess Playing Style Classification
#
# Responsibilities
# • Load Dataset
# • Remove Unnecessary Columns
# • Handle Missing Values
# • Encode Labels
# • Save Clean Dataset
#
# FINAL VERSION
# ==========================================

import pandas as pd

from sklearn.preprocessing import LabelEncoder


# ==========================================
# Paths
# ==========================================

INPUT_DATASET = "dataset/chess_dataset.csv"

OUTPUT_DATASET = "dataset/chess_dataset_clean.csv"


# ==========================================
# Columns to Remove
# ==========================================

REMOVE_COLUMNS = [

    "event",

    "site",

    "date",

    "white",

    "black",

    "eco"

]


# ==========================================
# Load Dataset
# ==========================================

def load_dataset():

    return pd.read_csv(INPUT_DATASET)


# ==========================================
# Remove Metadata
# ==========================================

def remove_metadata(df):

    existing = [

        column

        for column in REMOVE_COLUMNS

        if column in df.columns

    ]

    return df.drop(

        columns=existing

    )


# ==========================================
# Missing Values
# ==========================================

def handle_missing(df):

    numeric = df.select_dtypes(

        include=["number"]

    ).columns

    df[numeric] = df[numeric].fillna(0)

    categorical = df.select_dtypes(

        exclude=["number"]

    ).columns

    for column in categorical:

        df[column] = df[column].fillna("Unknown")

    return df


# ==========================================
# Encode Labels
# ==========================================

def encode_labels(df):

    encoder = LabelEncoder()

    df["Label"] = encoder.fit_transform(

        df["PrimaryStyle"]

    )

    return df, encoder


# ==========================================
# Save Dataset
# ==========================================

def save_dataset(df):

    df.to_csv(

        OUTPUT_DATASET,

        index=False

    )


# ==========================================
# Main
# ==========================================

def main():

    print()

    print("--------------------------------")

    print("Loading Dataset")

    print("--------------------------------")

    df = load_dataset()

    print(df.shape)

    print()

    df = remove_metadata(df)

    df = handle_missing(df)

    df, encoder = encode_labels(df)

    save_dataset(df)

    print("--------------------------------")

    print("Preprocessing Complete")

    print("--------------------------------")

    print("Output:")

    print(OUTPUT_DATASET)

    print()

    print("Labels:")

    for i, label in enumerate(encoder.classes_):

        print(i, "=", label)

    print("--------------------------------")


if __name__ == "__main__":

    main()

