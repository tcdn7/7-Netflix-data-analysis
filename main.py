import pandas as pd
import numpy as np

data_path = "data/netflix_titles.csv"
df = pd.read_csv(data_path)

print("==== BASIC DATASET INFO =====")
print(f"Dataset shape: {df.shape}")
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\n===== MISSING VALUES =====")
print(df.isna().sum())
