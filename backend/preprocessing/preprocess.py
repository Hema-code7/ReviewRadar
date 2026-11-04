import pandas as pd
from pathlib import Path


# Find the project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Dataset folder
DATASET_DIR = BASE_DIR / "dataset"

# Output folder for processed datasets
OUTPUT_DIR = DATASET_DIR / "processed"


def preprocess_dataset(file_name):
    file_path = DATASET_DIR / file_name

    # Load dataset
    df = pd.read_parquet(file_path)

    # Keep only required columns
    df = df[["text_", "label"]].copy()

    # Remove empty reviews
    df = df.dropna(subset=["text_"])
    df = df[df["text_"].str.strip() != ""]

    # Remove exact duplicate reviews
    df = df.drop_duplicates(subset=["text_"])

    # Convert labels
    df["label"] = df["label"].map({
        "OR": 0,
        "CG": 1
    })

    # Check for invalid labels
    if df["label"].isna().any():
        raise ValueError(f"Invalid labels found in {file_name}")

    # Rename columns
    df = df.rename(columns={"text_": "review_text"})

    return df


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = [
        "train.parquet",
        "validation.parquet",
        "test.parquet"
    ]

    for file_name in files:
        df = preprocess_dataset(file_name)

        output_name = file_name.replace(".parquet", "_processed.parquet")
        output_path = OUTPUT_DIR / output_name

        df.to_parquet(output_path, index=False)

        print(f"\nProcessed: {file_name}")
        print("Total reviews:", len(df))
        print("Label distribution:")
        print(df["label"].value_counts().sort_index())
        print("Saved to:", output_path)


if __name__ == "__main__":
    main()
